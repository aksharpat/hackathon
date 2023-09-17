import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image = cv2.imread("cropped_object_0.jpg")

# Convert the image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the lower and upper threshold values for green color in HSV
lower_green = np.array([30, 50, 50])  # Adjust these values as needed
upper_green = np.array([90, 255, 255])

# Create a mask for the green color
mask = cv2.inRange(hsv, lower_green, upper_green)

# Perform morphological operations to remove noise
kernel = np.ones((5, 5), np.uint8)
mask = cv2.erode(mask, kernel, iterations=1)
mask = cv2.dilate(mask, kernel, iterations=1)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours by area to remove small noise
min_contour_area = 100  # Adjust as needed
green_objects = [
    contour for contour in contours if cv2.contourArea(contour) > min_contour_area
]

# Create a blank image with a white background
height, width, _ = image.shape
blank_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background

# Draw bounding boxes around detected green objects on the blank image
for i, contour in enumerate(green_objects):
    # Find the minimum area rotated rectangle
    rect = cv2.minAreaRect(contour)

    # Get the corner points of the rotated rectangle
    box = cv2.boxPoints(rect)

    # Convert the coordinates to integers
    box = np.int0(box)

    # Draw the rotated rectangle on the blank image
    cv2.drawContours(blank_image, [box], 0, (0, 255, 0), 2)

# Create a scatter plot to visualize the detected green objects with bounding boxes
plt.figure(figsize=(8, 6))
plt.imshow(cv2.cvtColor(blank_image, cv2.COLOR_BGR2RGB))
plt.title("Detected Green Objects with Bounding Boxes")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
# plt.gca().invert_yaxis()  # Invert the y-axis to match image coordinates (0,0 at top-left)
plt.grid(True)
plt.show()
