# Import necessary libraries
from flask import Flask, render_template, request, flash, session, redirect, url_for
import mysql.connector
from mysql.connector import Error
import random
import re

# Initialize the Flask application
app = Flask(__name__)

# Set a secret key for session management (required for Flask sessions)
app.secret_key = 'your_secret_key'

# MySQL database connection settings
db_config = {
    'host': 'localhost',      # Database host
    'user': 'root',           # Database username
    'password': '@Ftsvolvl9', # Database password
    'database': 'OTP_database' # Database name
}

# Function to create a connection to the MySQL database
def create_database_connection():
    try:
        # Attempt to connect to the database using the provided configuration
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to 'OTP_database'")  # Print success message if connected
        return connection  # Return the connection object
    except Error as e:
        print("Error while connecting to 'OTP_database':", e)  # Print error message if connection fails
        return None  # Return None if connection fails

# Function to generate a random OTP (One-Time Password)
def generate_otp(length=5):
    # Generate a random OTP of the specified length (default is 5 digits)
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

# Route for the login page (handles both GET and POST requests)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''  # Initialize an empty message variable
    if request.method == 'POST':  # Check if the request method is POST
        username = request.form.get('username')  # Get username from the form
        password = request.form.get('password')  # Get password from the form
        entered_otp = request.form.get('otp')    # Get OTP from the form

        # Generate OTP only once when the user submits the login form
        if 'otp_generated' not in session:
            otp = generate_otp()  # Generate a new OTP
            session['otp'] = otp  # Store the OTP in the session
            flash(f'OTP generated! Please enter it: {otp}', 'info')  # Show OTP to the user
            session['otp_generated'] = True  # Mark that OTP has been generated

        # Connect to the database
        connection = create_database_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)  # Create a cursor to execute queries
            # Check if the username and password match a record in the database
            cursor.execute('SELECT * FROM user_data WHERE username = %s AND password = %s', (username, password))
            account = cursor.fetchone()  # Fetch the first matching record

            if account:  # If a matching account is found
                # Validate the OTP entered by the user
                if entered_otp:
                    if session['otp'] == entered_otp:  # Check if the entered OTP matches the session OTP
                        # Update session to indicate the user is logged in
                        session['loggedin'] = True
                        session['id'] = account['id']  # Store user ID in the session
                        session['username'] = account['username']  # Store username in the session
                        flash('Logged in successfully!', 'success')  # Show success message

                        # Clear OTP from the session after successful login
                        session.pop('otp', None)
                        session.pop('otp_generated', None)

                        # Update the database to clear the OTP (optional)
                        cursor.execute('UPDATE user_data SET otp = NULL WHERE id = %s', (account['id'],))
                        connection.commit()  # Commit the changes to the database

                        cursor.close()  # Close the cursor
                        connection.close()  # Close the connection
                        return redirect(url_for('dashboard'))  # Redirect to the dashboard
                    else:
                        msg = 'Invalid OTP. Please try again.'  # Show error message for invalid OTP
                else:
                    msg = 'Please enter the OTP sent to you.'  # Prompt the user to enter OTP
            else:
                msg = 'Incorrect username or password!'  # Show error message for invalid credentials

            cursor.close()  # Close the cursor
            connection.close()  # Close the connection

    # Render the login page and pass any messages or OTP to the template
    return render_template('login.html', msg=msg, otp=session.get('otp'))

# Route for the registration page (handles both GET and POST requests)
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''  # Initialize an empty message variable
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Get form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Connect to the database
        connection = create_database_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)  # Create a cursor to execute queries
            # Check if the username already exists in the database
            cursor.execute('SELECT * FROM user_data WHERE username = %s', (username,))
            account = cursor.fetchone()  # Fetch the first matching record

            if account:  # If the username already exists
                msg = 'Account already exists!'  # Show error message
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # Validate email format
                msg = 'Invalid email address!'  # Show error message
            elif not re.match(r'[A-Za-z0-9]+', username):  # Validate username format
                msg = 'Username must contain only characters and numbers!'  # Show error message
            else:
                # Insert the new user into the database
                cursor.execute('INSERT INTO user_data (username, password, email) VALUES (%s, %s, %s)',
                               (username, password, email))
                connection.commit()  # Commit the changes to the database
                msg = 'You have successfully registered!'  # Show success message

            cursor.close()  # Close the cursor
            connection.close()  # Close the connection

    # Render the registration page and pass any messages to the template
    return render_template('register.html', msg=msg)

# Route for the dashboard (accessible only to logged-in users)
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:  # Check if the user is logged in
        return render_template('index.html')  # Render the dashboard page
    else:
        return redirect(url_for('login'))  # Redirect to the login page if not logged in

# Route for logging out
@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect(url_for('login'))  # Redirect to the login page

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Start the app in debug mode and listen on all IP addresses