import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the breadboard image
breadboard_image = cv2.imread('breadboard5.jpg')

# Create a list of template images
template_paths = ['template10.jpg', 'template11.jpg', 'template12.jpg', 'template13.jpg']  # Add paths to your templates

# Set a threshold to determine matching locations
threshold = 0.8  # Adjust this threshold as needed

# Initialize an empty list to store detected hole positions
detected_holes_positions = []

# Iterate through each template
for template_path in template_paths:
    # Load the current template
    template = cv2.imread(template_path)

    # Perform template matching
    result = cv2.matchTemplate(breadboard_image, template, cv2.TM_CCOEFF_NORMED)

    # Find locations where the similarity score is above the threshold
    loc = np.where(result >= threshold)

    # Iterate through the detected locations and add them to the list
    for pt in zip(*loc[::-1]):
        detected_holes_positions.append(pt)

# Sort the detected hole positions by y-coordinate (row) and then by x-coordinate (column)
detected_holes_positions.sort(key=lambda x: (x[1], x[0]))

# Convert the list of positions into a 2D array
detected_holes_array = np.array(detected_holes_positions)

# Create a scatter plot to visualize the detected hole positions
plt.figure(figsize=(8, 6))
plt.scatter(detected_holes_array[:, 0], detected_holes_array[:, 1], c='red', marker='o', s=10)
plt.title('Detected Holes')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.gca().invert_yaxis()  # Invert the y-axis to match image coordinates (0,0 at top-left)
plt.grid(True)
plt.show()
