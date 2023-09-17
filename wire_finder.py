import cv2
import numpy as np

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

# Draw rotated rectangles around detected green objects on the original image
for contour in green_objects:
    # Find the minimum area rotated rectangle
    rect = cv2.minAreaRect(contour)

    # Convert rectangle parameters to integers
    box = np.int0(cv2.boxPoints(rect))

    # Draw the rotated rectangle on the original image
    cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

# Display the result
cv2.imwrite("wires_boxed.jpg", image)
cv2.imshow("Green Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
