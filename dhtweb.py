# Import necessary libraries
from flask import Flask, jsonify, render_template, request
import mysql.connector
from mysql.connector import Error


'''This code creates a Flask web application that interacts with a MySQL database to store and retrieve temperature and humidity data.
Database Connection: It establishes a connection to a MySQL server and creates a database (flask_database) and a table (dht_data) if they do not already exist.
Data Handling:
The /data route accepts POST requests containing JSON data with temperature and humidity readings. It saves this data to the MySQL database.
The / route fetches the latest 10 entries from the dht_data table and renders them in an HTML template (index.html).'''

# Create a Flask application instance
app = Flask(__name__)

# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Ftsvolvl9',  # Replace with your actual MySQL password
    'database': 'flask_database'  # Database name
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
            cursor.execute("CREATE DATABASE IF NOT EXISTS flask_database")
            print("Database 'flask_database' created or already exists.")
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
            print("Connected to 'flask_database'")
        return connection
    except Error as e:
        print("Error while connecting to 'flask_database':", e)
        return None

# Function to initialize the table
def initialize_table():
    connection = create_database_connection()
    if connection:
        cursor = connection.cursor()
        # SQL query to create the dht_data table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS dht_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature FLOAT,
            humidity FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'dht_data' created or already exists.")
        cursor.close()
        connection.close()

# Initialize the database and table on startup
create_database()
initialize_table()

# Route to handle data sent by the sensor
@app.route('/data', methods=['POST'])
def receive_dht_data():
    try:
        # Get the JSON data sent in the POST request
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        
        # Save data to MySQL
        connection = create_database_connection()
        if connection:
            cursor = connection.cursor()
            # SQL query to insert the received data into the dht_data table
            insert_query = "INSERT INTO dht_data (temperature, humidity) VALUES (%s, %s)"
            cursor.execute(insert_query, (temperature, humidity))
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
        cursor.execute("SELECT * FROM dht_data ORDER BY timestamp DESC LIMIT 10")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        # Render the index template with the fetched data
        return render_template('index.html', data=data)
    else:
        return jsonify({"error": "Failed to connect to the database"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')