# Import necessary libraries
import cv2
import urllib.request
import numpy as np

'''This code captures video from an IP camera using its URL and displays the live feed in a window using OpenCV.
Libraries Used:
cv2: OpenCV library for image and video processing.
urllib.request: Used to open the URL of the IP camera.
numpy: Used to handle the image data as an array.
Video Capture:
The cv2.VideoCapture object is created with the URL of the IP camera.
The code checks if the stream is opened successfully. If not, it prints an error message and exits.
Frame Reading:
The code enters a loop where it continuously reads frames from the IP camera.
It uses urllib.request.urlopen to fetch the image data from the camera's URL.
The image data is converted into a NumPy array and then decoded into an image format using cv2.imdecode.
Display: The decoded image is displayed in a window titled "live Cam Testing".
Exit Mechanism: The loop continues until the 'q' key is pressed, at which point the program exits the loop, releases the video capture object, and closes all OpenCV windows.'''

# Replace the URL with the IP camera's stream URL
url = 'http://192.168.43.235'  # Change this to your IP camera's URL
cv2.namedWindow("live Cam Testing", cv2.WINDOW_AUTOSIZE)  # Create a window to display the video

# Create a VideoCapture object to capture video from the IP camera
cap = cv2.VideoCapture(url)

# Check if the IP camera stream is opened successfully
if not cap.isOpened():
    print("Failed to open the IP camera stream")
    exit()

# Read and display video frames
while True:
    # Read a frame from the video stream using urllib
    img_resp = urllib.request.urlopen(url)  # Open the URL
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)  # Read the image data into a byte array
    im = cv2.imdecode(imgnp, -1)  # Decode the byte array into an image

    # Display the image in the created window
    cv2.imshow('live Cam Testing', im)

    # Wait for 5 milliseconds and check if 'q' key is pressed to exit
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()