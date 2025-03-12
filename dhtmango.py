# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime


'''This code creates a web application that receives temperature and humidity data from a sensor and stores it in a MongoDB database.
MongoDB Connection: The application connects to a MongoDB database named DHT_db and uses a collection named Sensor to store the sensor data.
'''
# Create a Flask application instance
app = Flask(__name__)

# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('localhost', 27017)

# Access the 'DHT_db' database and the 'Sensor' collection
db = client.DHT_db
Sensor = db.Sensor

# Route to handle data sent by the sensor
@app.route('/data', methods=['POST'])
def receive_dht_data():
    try:
        # Get JSON data from the request
        data = request.get_json()
        temperature = data.get('temperature')  # Extract temperature
        humidity = data.get('humidity')  # Extract humidity
        
        # Insert the data into the Sensor collection with a timestamp
        Sensor.insert_one({
            'temperature': temperature,
            'humidity': humidity,
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
        data = Sensor.find().sort('_id', -1).limit(10)
        
        # Convert the MongoDB cursor to a list
        data_list = list(data)

        # Render the template and pass the data to it
        return render_template('mongoDHT.html', data=data_list)
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
        data = Sensor.find().sort('_id', -1).limit(10)
        # Include timestamp in JSON response
        data_list = [{'temperature': entry['temperature'], 'humidity': entry['humidity'], 'timestamp': entry['timestamp'].isoformat()} for entry in data]
        return jsonify(data_list)
    except Exception as e:
        # Log any errors that occur
        print(f"Error fetching data: {e}")
        # Send an error response back to the client
        return jsonify({"error": "Failed to fetch data"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')