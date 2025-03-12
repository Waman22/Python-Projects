# Import necessary libraries
from flask import Blueprint, render_template  # Blueprint for modular Flask apps, render_template for rendering HTML
from pymongo import MongoClient  # MongoDB client for database interaction
from datetime import datetime  # For handling date and time

# Create a Blueprint for the admin module
# - 'admin': Name of the Blueprint
# - __name__: Helps Flask locate the Blueprint's resources
# - template_folder='templates': Specifies the folder where templates are stored
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

# Connect to MongoDB
# - MongoClient: Connects to the MongoDB server running on localhost at port 27017
client = MongoClient("mongodb://localhost:27017/")

# Access the database
# - "attendance_db": Name of the MongoDB database
db = client["attendance_db"]

# Access the collections
# - "users": Collection storing user data (e.g., employee_id, name)
# - "attendance_records": Collection storing attendance records (e.g., employee_id, status, timestamp)
users_collection = db["users"]
attendance_collection = db["attendance_records"]

# Route for the admin dashboard
@admin_blueprint.route('/dashboard')
def dashboard():
    """
    Fetches user and attendance data from MongoDB and renders it in the dashboard template.
    """
    # Fetch all users from the "users" collection
    users = list(users_collection.find())  # Convert cursor to a list of user documents

    # Get today's date and set the time to 00:00:00 for comparison
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch attendance records for today
    attendance_today = list(attendance_collection.find({
        "timestamp": {"$gte": today}  # Find records with timestamp greater than or equal to today
    }))  # Convert cursor to a list of attendance documents

    # Prepare attendance data for rendering
    attendance_data = []
    for user in users:
        # Find the attendance record for the current user (if any)
        record = next((r for r in attendance_today if r["employee_id"] == user["employee_id"]), None)

        # Determine the status and arrival time for the user
        if record:
            status = record["status"]  # Get the attendance status (e.g., "Present")
            arrival_time = record["timestamp"].strftime("%H:%M:%S")  # Format the timestamp as HH:MM:SS
        else:
            status = "Absent"  # If no record is found, mark the user as "Absent"
            arrival_time = "N/A"  # Set arrival time as "N/A"

        # Add the user's attendance data to the list
        attendance_data.append({
            "employee_id": user["employee_id"],  # Employee ID
            "name": user["name"],  # Employee name
            "status": status,  # Attendance status (Present/Absent)
            "arrival_time": arrival_time  # Arrival time or "N/A"
        })

    # Render the dashboard template with the attendance data
    return render_template('dashboard.html', attendance_data=attendance_data)