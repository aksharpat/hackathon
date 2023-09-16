import cv2 as cv
import numpy as np

# Load the image
image = cv.imread("breadboard.jpg")

if image is None:
    print("Error loading the image!")
    exit()

# Convert the image to grayscale
gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

# Apply Gaussian blur
blurred = cv.GaussianBlur(gray, (5, 5), 0)

# Edge detection using Canny
edges = cv.Canny(blurred, threshold1=30, threshold2=100)

# Find contours
contours, _ = cv.findContours(edges.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

# Assuming the largest contour corresponds to the outline of the breadboard
contour = sorted(contours, key=cv.contourArea, reverse=True)[0]

# Find the bounding rectangle of the largest contour
x, y, w, h = cv.boundingRect(contour)

# Crop the image to the bounding rectangle
cropped = image[y:y+h, x:x+w]

cv.imwrite("cropped_breadboard_2.jpg", cropped)

# Optional: Display the cropped image
cv.imshow("Cropped Breadboard", cropped)
cv.waitKey(0)
cv.destroyAllWindows()
