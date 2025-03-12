# Import necessary libraries
from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error


'''This code creates a web application that receives sensor data (temperature, humidity, and moisture) and stores it in a MySQL database.
MySQL Connection: The application connects to a MySQL database named Soil_database and uses a table named Sensor_data to store the sensor readings.
'''

# Create a Flask application instance
app = Flask(__name__)

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Ftsvolvl9',  # Replace with your actual MySQL password
    'database': 'Soil_database'  # Database name
}

# Function to connect to MySQL server without specifying a database
def create_server_connection():
    try:
        # Establish a connection to the MySQL server
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Connected to MySQL server")
        return connection
    except Error as e:
        print("Error while connecting to MySQL server:", e)
        return None

# Function to create the database if it doesn't exist
def create_database():
    connection = create_server_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS Soil_database")
            print("Database 'Soil_database' created or already exists.")
            connection.commit()
        except Error as e:
            print("Error while creating database:", e)
        finally:
            cursor.close()
            connection.close()

# Function to connect to the specified database
def create_database_connection():
    try:
        # Establish a connection to the specified database
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to 'Soil_database'")
        return connection
    except Error as e:
        print("Error while connecting to 'Soil_database':", e)
        return None

# Function to initialize the table
def initialize_table():
    connection = create_database_connection()
    if connection:
        cursor = connection.cursor()
        # SQL query to create the Sensor_data table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Sensor_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature FLOAT,
            humidity FLOAT,
            moisture FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'Sensor_data' created or already exists.")
        cursor.close()
        connection.close()

# Initialize the database and table on startup
create_database()
initialize_table()

# Route to handle data sent by the sensor
@app.route('/data', methods=['POST'])
def receive_dht_data():
    try:
        # Get JSON data from the request
        data = request.get_json()
        temperature = data.get('temperature')  # Extract temperature
        humidity = data.get('humidity')  # Extract humidity
        moisture = data.get('Moisture')  # Extract moisture
        
        # Save data to MySQL
        connection = create_database_connection()
        if connection:
            cursor = connection.cursor()
            # SQL query to insert the received data into the Sensor_data table
            insert_query = "INSERT INTO Sensor_data (temperature, humidity, moisture) VALUES (%s, %s, %s)"
            cursor.execute(insert_query, (temperature, humidity, moisture))
            connection.commit()
            cursor.close()
            connection.close()
        
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
    # Fetch the latest 10 entries from the database
    connection = create_database_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Sensor_data ORDER BY timestamp DESC LIMIT 10")
        data = cursor.fetchall()  # Fetch all results
        cursor.close()
        connection.close()
        # Render the template and pass the data to it
        return render_template('soil.html', data=data)
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')