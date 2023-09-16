import cv2
import numpy as np

# Load the breadboard image
breadboard_image = cv2.imread('breadboard3.jpg')

# Load the template (square hole) image
template = cv2.imread('template.jpg')

# Perform template matching
result = cv2.matchTemplate(breadboard_image, template, cv2.TM_CCOEFF_NORMED)

# Set a threshold to determine matching locations
threshold = 0.8  # Adjust this threshold as needed

# Find locations where the similarity score is above the threshold
loc = np.where(result >= threshold)

# Draw rectangles around detected holes
for pt in zip(*loc[::-1]):
    cv2.rectangle(breadboard_image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)
cv2.imwrite('detected_holes.jpg', breadboard_image)
# Display the result
cv2.imshow('Detected Holes', breadboard_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
