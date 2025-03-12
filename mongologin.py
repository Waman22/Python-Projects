# Import necessary libraries
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient

# Create a Flask application instance
app = Flask(__name__)

'''The application uses Flask to create a web application that allows users to sign up, log in, and access a dashboard.
It connects to a MongoDB database to store user information.'''

# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('localhost', 27017)

# Access the 'flask_db' database from the MongoDB client
db = client.Mongo.flask_db

# Access the 'Signup' collection within the 'flask_db' database
Signup = db.Signup

# Define the home route
@app.route("/", methods=['POST', 'GET'])
def home():
    # Render the layout template for the home page
    return render_template('layout.html')

# Define the signup route
@app.route("/sign", methods=['POST', 'GET'])
def sign():
    if request.method == 'POST':
        # Retrieve form data from the signup form
        name = request.form['name']
        surname = request.form['surname']
        username = request.form['username']
        password = request.form['password']
        Date = request.form['Dob']
        email = request.form['email']
        Address = request.form['Address']
        
        # Insert the new user data into the Signup collection
        Signup.insert_one({
            'name': name,
            'surname': surname,
            'username': username,
            'password': password,
            'Date': Date,
            'email': email,
            'Address': Address,
        })
        
        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    # Render the signup template for GET requests
    return render_template('signup.html')

# Define the login route
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Retrieve form data from the login form
        username = request.form['username']
        password = request.form['password']
        
        # Select a single user document by username from the Signup collection
        user = Signup.find_one({'username': username})

        # Check if the user exists and if the password matches
        if user and user['password'] == password:
            # Redirect to the dashboard if login is successful
            return redirect(url_for('dashboard', username=username))
        else:
            # Display an error message if login fails
            incorrect = "Username or Password is incorrect! Try again or Sign Up."
            return render_template("login.html", erro=incorrect)
    else:
        # Render the login template for GET requests
        return render_template("login.html")

# Define the dashboard route
@app.route('/dashboard/<username>', methods=['POST', 'GET'])
def dashboard(username):
    # Render the dashboard template, passing the username to it
    return render_template("dashboard.html", username=username)

# Define the logout route
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # Render the login template when the user logs out
    return render_template("login.html")

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')