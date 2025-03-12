# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Create a Flask application instance
app = Flask(__name__)
'''This code creates a web application that receives soil sensor data (temperature, humidity, and moisture) and stores it in a MongoDB database.
MongoDB Connection: The application connects to a MongoDB database named Soil_db and uses a collection named Soil to store the sensor readings.
'''
# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('localhost', 27017)

# Access the 'Soil_db' database and the 'Soil' collection
db = client.Soil_db
Soil = db.Soil

# Route to handle data sent by the sensor
@app.route('/data', methods=['POST'])
def receive_dht_data():
    try:
        # Get JSON data from the request
        data = request.get_json()
        temperature = data.get('temperature')  # Extract temperature
        humidity = data.get('humidity')  # Extract humidity
        moisture = data.get('Moisture')  # Extract moisture
        
        # Insert the data into the Soil collection with a timestamp
        Soil.insert_one({
            'temperature': temperature,
            'humidity': humidity,
            'moisture': moisture,
            'timestamp': datetime.now()  # Current date and time
        })
        
        # Send a success response back to the client
        return jsonify({"status": "success", "data": data}), 200
    except Exception as e:
        # Log any errors that occur
        print(f"Error: {e}")
        # Send an error response back to the client
        return jsonify({"status": "error", "message": str(e)}), 400

# Route to display the data in an HTML file
@app.route('/')
def index():
    try:
        # Fetch the latest 10 entries from the database, sorted by _id in descending order
        data = Soil.find().sort('_id', -1).limit(10)
        
        # Convert the MongoDB cursor to a list
        data_list = list(data)

        # Render the template and pass the data to it
        return render_template('send.html', data=data_list)
    except Exception as e:
        # Log any errors that occur
        print(f"Error fetching data: {e}")
        # Send an error response back to the client
        return jsonify({"error": "Failed to fetch data"}), 500

# Route to get the latest 10 entries for the chart
@app.route('/latest-data')
def latest_data():
    try:
        # Fetch the latest 10 entries from the database
        data = Soil.find().sort('_id', -1).limit(10)
        # Include timestamp in JSON response
        data_list = [{'temperature': entry['temperature'], 'humidity': entry['humidity'], 'moisture': entry['moisture'], 'timestamp': entry['timestamp'].isoformat()} for entry in data]
        return jsonify(data_list)
    except Exception as e:
        # Log any errors that occur
        print(f"Error fetching data: {e}")
        # Send an error response back to the client
        return jsonify({"error": "Failed to fetch data"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')