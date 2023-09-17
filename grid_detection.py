import cv2
import numpy as np

# Load the breadboard image
breadboard_image = cv2.imread('breadboard8.jpg')

# Create a list of template images
template_paths = ['template10.jpg','template11.jpg','template12.jpg','template13.jpg','template14.jpg','template15.jpg','template16.jpg','template17.jpg']  # Add paths to your templates

# Set a threshold to determine matching locations
threshold = 0.75  # Adjust this threshold as needed
detected_holes_positions = []

# Iterate through each template
for template_path in template_paths:
    # Load the current template
    template = cv2.imread(template_path)

    # Perform template matching
    result = cv2.matchTemplate(breadboard_image, template, cv2.TM_CCOEFF_NORMED)

    # Find locations where the similarity score is above the threshold
    loc = np.where(result >= threshold)

    # Draw rectangles around detected holes
    for pt in zip(*loc[::-1]):
        cv2.rectangle(breadboard_image, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (0, 255, 0), 2)

# Save the result to a JPG file
cv2.imwrite('detected_holes.jpg', breadboard_image)

# Display the result
cv2.imshow('Detected Holes', breadboard_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
