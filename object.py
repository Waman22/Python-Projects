# Import necessary libraries
from ultralytics import YOLO
import cv2
import math 
'''This code uses the YOLOv8 model to perform real-time object detection from a webcam feed.
Webcam Initialization: The code initializes the webcam and sets the resolution to 640x480 pixels.
Model Loading: The YOLO model is loaded from the specified weights file (yolov8n.pt).
Object Classes: The code defines a list of object classes that the model can detect, based on the COCO dataset.
Frame Processing:
The code enters a loop where it continuously captures frames from the webcam.
Each frame is processed by the YOLO model to detect objects.
For each detected object, the bounding box is drawn, and the confidence score and class name are printed to the console.
Display: The processed frame with detected objects is displayed in a window titled "Webcam".
Exit Mechanism: The loop continues until the 'q' key is pressed, at which point the video capture is released, and all OpenCV windows are closed.'''
''' This code is for real-time object detection using YOLO. '''

# Start webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam
cap.set(3, 640)  # Set the width of the video frame
cap.set(4, 480)  # Set the height of the video frame

# Load the YOLO model
model = YOLO("yolo-Weights/yolov8n.pt")  # Load the YOLOv8 model weights

# Object classes (COCO dataset classes)
classNames = [
    "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
    "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
    "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
    "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
    "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
    "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
    "teddy bear", "hair drier", "toothbrush"
]

# Main loop for processing video frames
while True:
    success, img = cap.read()  # Capture a frame from the webcam
    results = model(img, stream=True)  # Perform object detection on the frame

    # Process the results
    for r in results:
        boxes = r.boxes  # Get the bounding boxes from the results

        for box in boxes:
            # Get bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Convert to integer values

            # Draw the bounding box on the image
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Get confidence score
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)

            # Get class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            # Prepare to display object details
            org = [x1, y1]  # Origin for text placement
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)  # Color for text
            thickness = 2

            # Put the class name on the image
            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    # Display the processed frame
    cv2.imshow('Webcam', img)

    # Exit the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()