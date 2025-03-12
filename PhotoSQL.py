import os
import sqlite3

'''The code connects to an SQLite database named example.db. If the database file does not exist, it will be created.
Table Creation: A table named images is created to store image data. The table has three columns: id (an auto-incrementing primary key), name (the name of the image file), and data (the binary data of the image).
Function to Save Images:
The save_images_from_folder function takes a folder path as an argument.
It checks if the specified folder exists. If not, it prints an error message and exits the function.
It iterates through all files in the specified folder, checking if each item is a file.
For each file, it opens the file in binary read mode, reads the data, and inserts the filename and data into the database.
If an error occurs during the insertion, it prints an error message.
Commit Changes: After processing all files, the changes are committed to the database.
Close Connection: Finally, the database connection is closed.'''

# Connect to SQLite database (creates the database file if it doesn't exist)
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# Create a table for storing images if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    data BLOB NOT NULL
)
''')
conn.commit()  # Commit the changes to the database

# Function to save images from a folder to the database
def save_images_from_folder(folder_path):
    # Check if the specified folder exists
    if not os.path.exists(folder_path):
        print(f"The folder path '{folder_path}' does not exist.")
        return
    
    # Iterate through all files in the specified folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)  # Get the full file path
        if os.path.isfile(file_path):  # Ensure it's a file
            with open(file_path, 'rb') as file:  # Open the file in binary read mode
                blob_data = file.read()  # Read the file data
            try:
                # Insert the filename and file data into the database
                cursor.execute('INSERT INTO images (name, data) VALUES (?, ?)', (filename, blob_data))
                print(f"Saved {filename} to database.")
            except sqlite3.Error as e:
                print(f"Error saving {filename}: {e}")  # Print any errors that occur during insertion
    
    conn.commit()  # Commit the changes to the database
    print("All images saved successfully!")

# Specify the folder containing images
folder_path = 'static/images'  # Replace with your actual folder path
save_images_from_folder(folder_path)  # Call the function to save images

# Close the database connection
conn.close()