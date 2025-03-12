# Import necessary libraries
from flask import Flask, render_template, request, jsonify
from geopy.distance import geodesic  # To calculate distance

# Create a Flask application instance
app = Flask(__name__)

'''This code creates a simple web application that checks if a user is at a specific geographic location based on latitude and longitude.
Target Location: The application defines a target location (latitude and longitude) and an allowed radius (50 meters) within which the user must be to be considered "at the correct location."
'''

# Define the correct location (latitude, longitude)
TARGET_LOCATION = (-26.205647, 28.0337185)  # Change this to your required location
ALLOWED_RADIUS = 0.05  # 50 meters (adjust as needed)

# Route for the home page
@app.route('/')
def index():
    # Render the location input page
    return render_template('location.html')

# Route to handle location data sent by the client
@app.route('/location', methods=['POST'])
def get_location():
    # Get JSON data from the request
    data = request.json
    user_lat = data.get('latitude')  # Extract latitude from the data
    user_lon = data.get('longitude')  # Extract longitude from the data

    if user_lat and user_lon:
        # Convert user latitude and longitude to a tuple
        user_location = (float(user_lat), float(user_lon))
        
        # Calculate the distance from the user's location to the target location
        distance = geodesic(user_location, TARGET_LOCATION).km  # Get distance in km

        # Check if the user is within the allowed radius
        if distance <= ALLOWED_RADIUS:
            message = "Thank you! You are at the correct location."
            status = "success"
            print(message, status)
        else:
            message = " You must be at the correct location to log in."
            status = "error"
            print(message, status)

        # Return a JSON response with the status and distance information
        return jsonify({
            "status": status,
            "latitude": user_lat,
            "longitude": user_lon,
            "distance_km": round(distance, 3),
            "message": message
        })

    # Return an error response if location data is not received
    return jsonify({"status": "error", "message": "Location not received"}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)