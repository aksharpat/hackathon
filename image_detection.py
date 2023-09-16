import cv2
import numpy as np

# Load the image
image = cv2.imread("breadboard.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise and enhance contours
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Perform edge detection
edges = cv2.Canny(blurred, threshold1=30, threshold2=100)
cv2.imshow("edge Breadboard", edges)
# Find contours in the edge-detected image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort the contours by area in descending order and keep the largest one
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

# Create a mask for the largest contour
mask = np.zeros_like(gray)
cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

# Bitwise-AND the mask with the original image to extract the breadboard region
breadboard_only = cv2.bitwise_and(image, image, mask=mask)

# Save or display the cropped breadboard image
cv2.imwrite("cropped_breadboard.jpg", breadboard_only)
# cv2.imshow("Cropped Breadboard", breadboard_only)
cv2.waitKey(0)
cv2.destroyAllWindows()
