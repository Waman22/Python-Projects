from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import qrcode
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# MySQL connection settings
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '@Ftsvolvl9',
    'database': 'Inventory_database'
}

# Function to connect to MySQL server without specifying a database
def create_server_connection():
    try:
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
            cursor.execute("CREATE DATABASE IF NOT EXISTS Inventory_database")
            print("Database 'Inventory_database' created or already exists.")
        except Error as e:
            print("Error while creating database:", e)
        finally:
            cursor.close()
            connection.close()

# Function to connect to the specified database
def create_database_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to 'Inventory_database'")
        return connection
    except Error as e:
        print("Error while connecting to 'Inventory_database':", e)
        return None

def init_db():
    conn = create_database_connection()
    if conn:
        try:
            c = conn.cursor()

            # Create Available_TOOLS table
            c.execute('''CREATE TABLE IF NOT EXISTS Available_TOOLS (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        Tool_name VARCHAR(255) NOT NULL,
                        location VARCHAR(255),
                        qr_code_path VARCHAR(255)
                        )''')

            # Create Tool_Acqusition table
            c.execute('''CREATE TABLE IF NOT EXISTS Tool_Acqusition (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tool_id INT,
                        worker_id INT NOT NULL,
                        date DATE NOT NULL,
                        location VARCHAR(255),
                        action ENUM('Take-Tools', 'Return-Tools') NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        status ENUM('Available', 'In Use') DEFAULT 'Available',
                        FOREIGN KEY (tool_id) REFERENCES Available_TOOLS(id)
                        )''')

            # Create ADD_TOOLS table
            c.execute('''CREATE TABLE IF NOT EXISTS Available_TOOLS (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name TEXT NOT NULL,
                        photo BLOB NOT NULL,
                        File_info TEXT NOT NULL,
                        location TEXT NOT NULL,
                        tool_name TEXT NOT NULL,
                        date TEXT NOT NULL
                        )''')

            # Create workers table
            c.execute('''CREATE TABLE IF NOT EXISTS workers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        worker_id VARCHAR(50) UNIQUE,  
                        name VARCHAR(50) NOT NULL,
                        surname VARCHAR(50) NOT NULL,
                        dob DATE NOT NULL,
                        email VARCHAR(100) NOT NULL UNIQUE,
                        cellphone VARCHAR(20) NOT NULL,  
                        id_number VARCHAR(50) NOT NULL,  
                        course VARCHAR(100) NOT NULL,
                        specialization VARCHAR(100) NOT NULL,
                        address TEXT NOT NULL,
                        cohort VARCHAR(50) NOT NULL,
                        UNIQUE(name, surname))''')

            # Create Damaged_Tools table
            c.execute('''CREATE TABLE IF NOT EXISTS Damaged_Tools (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        tool_id INT,
                        worker_id INT NOT NULL,
                        date DATE NOT NULL,
                        location VARCHAR(255),
                        action ENUM('Check-Out', 'Check-In') NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (tool_id) REFERENCES Available_TOOLS(id)
                        )''')
            
            # Commit changes
            conn.commit()
            
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()

     
def add_sample_workers():
    conn = create_database_connection()  # Connect to the NEW_WORKERS_database
    if conn:
        try:
            c = conn.cursor()

            # Connect to Worker_database for retrieving employee data
            worker_db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '@Ftsvolvl9',
                'database': 'Worker_database'  # Change this to the correct database where employees are stored
            }

            # Establish a new connection to Worker_database
            worker_conn = mysql.connector.connect(**worker_db_config)

            if worker_conn:
                worker_cursor = worker_conn.cursor()

                # Ensure the employees table exists in Worker_database
                worker_cursor.execute('''SHOW TABLES LIKE 'employees';''')
                result = worker_cursor.fetchone()

                if result:
                    print("Employees table exists, proceeding with data insertion.")

                    # Insert data from Worker_database.employees into NEW_WORKERS_database.workers
                    worker_cursor.execute('''SELECT worker_id, name, surname, dob, email, cellphone, id_number, course, specialization, address, cohort
                                              FROM employees''')
                    employees_data = worker_cursor.fetchall()

                    # Insert the fetched employee data into the workers table
                    for employee in employees_data:
                        c.execute('''INSERT IGNORE INTO workers (worker_id, name, surname, dob, email, cellphone, id_number, course, specialization, address, cohort)
                                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', employee)

                    conn.commit()
                    print("Data inserted successfully.")
                else:
                    print("Error: 'employees' table does not exist in Worker_database.")
                
                # Close Worker_database connection
                worker_cursor.close()
                worker_conn.close()

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            conn.close()
            
            
# Define the directory to save images
UPLOAD_FOLDER = 'static/images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def generate_qr_code(data, filename):
    """Generates a QR code and saves it to a file."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="green", back_color="white")
    
    # Save the image to the specified directory
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(file_path)
    return file_path
def save_qr_to_db(name, file_path, location, tool, date):
    """Saves the QR code image and details to the MySQL database."""
    conn = create_database_connection()
    if conn:
        try: 
            # Read the QR code image as binary data
            with open(file_path, 'rb') as file:
                blob_data = file.read()
            
            cursor = conn.cursor()
            
            # Insert into ADD_TOOLS table
            cursor.execute(''' 
                INSERT INTO ADD_TOOLS (name, photo, File_info, location, tool_name, date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (name, blob_data, file_path, location, tool, date))
            conn.commit()

            # Insert into Available_TOOLS table (store file path in qr_code_path)
            cursor.execute('''
                INSERT INTO Available_TOOLS (Tool_name, location, qr_code_path)
                VALUES (%s, %s, %s)
            ''', (tool, location, file_path))  # Use file_path as the qr_code_path
            conn.commit()
            
        except mysql.connector.Error as err:
            print(f"Error inserting data: {err}")
            conn.rollback()
        finally:
            conn.close()

        
'''this route is the dashboard page it will be the first page to appear to users and ask them if they want to take a tool'''
@app.route('/')
def home():
    if request.method == 'POST':
        # Get form data from the user
        Take_tools = request.form['Take_tools']
        Return_tools = request.form['Return_tools']
        
        if Take_tools:
            redirect(Take_tools)
            
        if Return_tools:
            redirect(Return_tools)
            
        else:
            return redirect(url_for('home'))
        
    return render_template('ToolSystem.html')  # Render a form to select tools

@app.route('/Take_tools', methods=['GET', 'POST'])
def Take_tools():
    if request.method == 'POST':
        # Get form data from the user
        worker_id = request.form['worker_id']
        selected_tools = request.form.getlist('selected_tools')  # List of tool IDs
        location = request.form['location']
        Type = request.form['Type']
        date = request.form['date']
        action = 'Take-Tools'  # Default action for taking tools
        
        # Store form data in session for access on the scan page
        session['worker_id'] = worker_id
        session['selected_tools'] = selected_tools
        session['location'] = location
        session['Type'] = Type
        session['date'] = date

        # Redirect to the scan page
        return redirect(url_for('scan'))

    conn = create_database_connection()
    if conn:
            try:
                cursor = conn.cursor()

                # Insert data into the Tool_Acqusition table
                for tool_id in selected_tools:
                    cursor.execute('''
                        INSERT INTO Tool_Acqusition (tool_id, worker_id, date, location,Type, action, status)
                        VALUES (%s, %s, %s, %s, %s, %s,%s)
                    ''', (tool_id, worker_id, date, location,Type, action, 'In Use'))

                    # Update the status of the tool in Available_TOOLS table
                    cursor.execute('''
                        UPDATE Available_TOOLS
                        SET status = 'In Use'
                        WHERE id = %s
                    ''', (tool_id,))

                conn.commit()
                flash("Tools checked out successfully!", "success")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.rollback()
                flash("An error occurred while checking out tools.", "danger")
            finally:
                conn.close()

            return redirect(url_for('home'))  # Redirect to the dashboard after processing

    # Fetch available tools for the form
    conn = create_database_connection()
    available_tools = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, Tool_name
                FROM Available_TOOLS
                                WHERE status = 'Available'
            ''')
            available_tools = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Error fetching available tools: {err}")
        finally:
            conn.close()

    return render_template('Take_tools.html', available_tools=available_tools)





@app.route('/Return_tools')
def Return_tools():
    # Here, we could fetch available tools from the database
    conn = create_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Tool_name, location FROM Available_TOOLS WHERE status = 'Available'")
    tools = cursor.fetchall()
    conn.close()
    
    return render_template('view_tools.html', tools=tools)



@app.route('/Dashboard', methods=['GET', 'POST'])
def Dashboard():
    if request.method == 'POST':
        # Get form data from the user
        ADD_tools = request.form['ADD_tools']
        Delete_tools = request.form['Delete_tools']
        
        if ADD_tools:
            redirect(Add_Tools)
            
        if Delete_tools:
            redirect(Delete_tools)
            
        else:
            return redirect(url_for('Dashboard'))
        
    return render_template('DASHBOARD.html')  # Render a form to select tools
        

@app.route('/ADD_Tools', methods=['GET', 'POST'])
def Add_Tools():
    if request.method == 'POST':
        # Get form data from the user
        File_info = request.form['File_info']
        location = request.form['location']
        tool = request.form['tool']
        date = request.form['date']

        # Prepare the data string
        data = f"Department: {location} workshop,\n Tool Name : {tool}\n Entry Date: {date}"

        # Generate QR code and save its
        filename = f"qr_code_{File_info}.png"
        file_path = generate_qr_code(data, filename)

        # Save the QR code and details in the database
        save_qr_to_db(filename, file_path, location, tool, date)

        # Return the URL of the saved image (can be accessed via Flask's static folder)
        return render_template('ADD_QR.html', qr_code_image=filename)

    return render_template('ADD_QR.html', qr_code_image=None)




@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        # Retrieve stored session data
        worker_id = session.get('worker_id')
        selected_tools = session.get('selected_tools', [])
        location = session.get('location')
        Type = session.get('Type')
        date = session.get('date')
        action = 'Take-Tools'

        conn = create_database_connection()
        if conn:
            try:
                cursor = conn.cursor()

                # Insert data into the Tool_Acqusition table and update the tool status
                for tool_id in selected_tools:
                    cursor.execute('''
                        INSERT INTO Tool_Acqusition (tool_id, worker_id, date, location, Type, action, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (tool_id, worker_id, date, location, Type, action, 'In Use'))

                    cursor.execute('''
                        UPDATE Available_TOOLS
                        SET status = 'In Use'
                        WHERE id = %s
                    ''', (tool_id,))

                conn.commit()
                flash("Tools successfully registered and scanned!", "success")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                conn.rollback()
                flash("An error occurred while registering tools.", "danger")
            finally:
                conn.close()

            return redirect(url_for('home'))  # Redirect to the dashboard or another page after scanning

    return render_template('scan.html')  # Render the scan page


if __name__ == "__main__":
    create_database()
    init_db()
    add_sample_workers()
    app.run(debug=True)
