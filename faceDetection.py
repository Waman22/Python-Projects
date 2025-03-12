# Import the OpenCV library
import cv2


'''This code uses OpenCV's Haar cascade classifier to detect faces in real-time from a video stream (either from a webcam or a video file).
Haar Cascade: The Haar cascade for frontal face detection is loaded using OpenCV's built-in data.
Video Capture: The code initializes video capture from the default webcam (or a specified video file).
Frame Processing:
Each frame is captured in a loop.
The frame is converted to grayscale, which is required for the Haar cascade to work.
The detectMultiScale method is used to detect faces in the grayscale image. It returns a list of rectangles where faces are detected.
Drawing Rectangles: For each detected face, a rectangle is drawn around it in the original frame.
Display: The processed frame with detected faces is displayed in a window titled "Face Detection".
Exit Mechanism: The loop continues until the 'q' key is pressed, at which point the video capture is released, and all OpenCV windows are closed.'''

# Load the Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the video capture (use 0 for the default webcam, or provide a video file path)
cap = cv2.VideoCapture(0)

''' 
This code is for detecting faces only; it does not identify whose face it is.
'''

while True:
    # Capture each frame from the video
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture video.")
        break

    # Convert the frame to grayscale (required for Haar cascade)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Display the frame with detected faces
    cv2.imshow("Face Detection", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()