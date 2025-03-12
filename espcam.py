# Import the OpenCV library
import cv2
'''This code uses the YOLO (You Only Look Once) algorithm to perform real-time object detection on video frames captured from a webcam or video file.
Loading YOLO Model: The model weights (yolov3.weights) and configuration file (yolov3.cfg) are loaded to initialize the YOLO network.
Video Capture: The code captures video from a webcam (or a video file if specified).
Frame Processing:
Each frame is preprocessed to create a blob that can be fed into the YOLO model.
The model performs a forward pass to get the output from the output layers.
Detection Processing:
The code iterates through the detections and checks the confidence score.
If the confidence score exceeds a threshold (0.5 in this case), it calculates the bounding box coordinates and draws a rectangle around the detected object.
A label ("Object") is added above the bounding box.
Display: The processed frame with detections is displayed in a window.
Exit Mechanism: The loop continues until the 'q' key is pressed, at which point the video capture is released and all OpenCV windows are closed.'''
# Load YOLO model weights and configuration
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

# Get the names of the layers in the YOLO model
layer_names = net.getLayerNames()

# Get the output layers (the layers that produce the output)
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Capture video from a file or webcam (0 for webcam)
cap = cv2.VideoCapture(0)

# Main loop to process video frames
while True:
    # Read a frame from the video capture
    ret, frame = cap.read()
    if not ret:
        break  # Exit the loop if no frame is captured

    # Get the dimensions of the frame
    height, width, _ = frame.shape
    
    # Preprocess the frame for YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)  # Set the input to the network
    outs = net.forward(output_layers)  # Perform forward pass to get output

    # Process detections
    for detection in outs:
        for object in detection:
            confidence = object[5]  # Get the confidence score
            if confidence > 0.5:  # Set a confidence threshold
                # Object detected
                center_x = int(object[0] * width)  # Calculate center x coordinate
                center_y = int(object[1] * height)  # Calculate center y coordinate
                w = int(object[2] * width)  # Calculate width of the bounding box
                h = int(object[3] * height)  # Calculate height of the bounding box
                x = int(center_x - w / 2)  # Calculate top-left x coordinate
                y = int(center_y - h / 2)  # Calculate top-left y coordinate
                
                # Draw bounding box around the detected object
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Put text label above the bounding box
                cv2.putText(frame, 'Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Display the frame with detections
    cv2.imshow('Object Recognition', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()