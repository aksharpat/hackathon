import cv2
import numpy as np

# Load the image
image = cv2.imread("cropped_object_0.jpg")

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to make holes more distinct
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area
holes = []

for contour in contours:
    area = cv2.contourArea(contour)
    if area > 10:  # Adjust this threshold as needed
        holes.append(contour)

# Draw contours on the original image (optional)
cv2.drawContours(image, holes, -1, (0, 255, 0), 2)  # Draw green contours

# Display the result (optional)
cv2.imshow("Detected Holes", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Access hole coordinates
hole_centers = []

for contour in holes:
    # Calculate the centroid of the contour
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        hole_centers.append((cx, cy))

# Print hole coordinates
for i, (cx, cy) in enumerate(hole_centers):
    print(f"Hole {i+1}: X={cx}, Y={cy}")
cv2.imwrite("cropped2_breadboard.jpg", image)
