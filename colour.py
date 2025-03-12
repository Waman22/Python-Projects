# Import necessary libraries
import cv2
import numpy as np

'''This code uses OpenCV to perform color detection on an image.
Image Loading: The image is loaded from a specified file path.
Color Space Conversion: The image is converted from BGR (the default color space for OpenCV) to HSV (Hue, Saturation, Value) color space, which is often more effective for color detection.
Color Range Definition: The code defines specific HSV ranges for detecting red, blue, and green colors. Red is defined with two ranges to account for the circular nature of the hue component in HSV.
Mask Creation: Masks are created for each color using the cv2.inRange function, which creates a binary mask where the pixels within the specified color range are set to 255 (white) and all other pixels are set to 0 (black).
Mask Combination: The individual masks for red, blue, and green are combined into a single mask.
Result Generation: The combined mask is applied to the original image using a bitwise AND operation, resulting in an image that highlights the detected colors.
Display Results: The original image, the combined mask, and the result of the color detection are displayed in separate windows.
Window Management: The program waits for a key press before closing all OpenCV windows.'''

# Load an image from the specified path
image = cv2.imread('static/image/image/21.jpg', cv2.IMREAD_COLOR)


# Convert the image from BGR color space to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define color ranges for detection in HSV color space
# Red color range (two ranges to cover the hue wrap-around)
lower_red1 = np.array([0, 120, 70])
upper_red1 = np.array([10, 255, 255])

lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Blue color range
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

# Green color range
lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])

# Create masks for each color using the defined ranges
mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
mask_green = cv2.inRange(hsv, lower_green, upper_green)

# Combine the masks for red, blue, and green colors
combined_mask = mask_red | mask_blue | mask_green

# Apply the combined mask to the original image using bitwise AND
result = cv2.bitwise_and(image, image, mask=combined_mask)

# Display the original image, the combined mask, and the detected objects
cv2.imshow("Original Image", image)
cv2.imshow("Combined Mask", combined_mask)
cv2.imshow("Detected Objects", result)

# Wait indefinitely until a key is pressed, then close all OpenCV windows
cv2.waitKey(0)
cv2.destroyAllWindows()