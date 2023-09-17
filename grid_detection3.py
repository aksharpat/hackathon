import cv2
import numpy as np
import matplotlib.pyplot as plt

def non_max_suppression(rectangles, min_distance):
    if len(rectangles) == 0:
        return []

    # Convert rectangles to (x, y) format
    rectangles = np.array(rectangles)

    # Sort rectangles by x-coordinate
    rectangles = rectangles[np.argsort(rectangles[:, 0])]

    # Initialize the list of picked rectangles
    picked_rectangles = [rectangles[0]]

    for rect in rectangles[1:]:
        # Check if the current rectangle is far enough from the picked rectangles
        distances = np.sqrt(np.sum(np.square(picked_rectangles - rect), axis=1))
        if np.min(distances) >= min_distance:
            picked_rectangles.append(rect)

    return picked_rectangles

# Load the breadboard image
breadboard_image = cv2.imread('breadboard9.jpg')

# Create a list of template images
template_paths = ['template10.jpg','template11.jpg','template12.jpg','template13.jpg','template14.jpg','template15.jpg','template16.jpg','template17.jpg']  # Add paths to your templates


# Set a threshold to determine matching locations
threshold = 0.77  # Adjust this threshold as needed
min_distance = 50  # Minimum distance between detected holes

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

# Apply non-maximum suppression to remove overlapping detections
detected_holes_positions = non_max_suppression(detected_holes_positions, min_distance=min_distance)

# Create a 2D array to store the detected hole positions
detected_holes_array = np.array(detected_holes_positions)

# Calculate the bounding box of all detected holes
x_values = detected_holes_array[:, 0]
y_values = detected_holes_array[:, 1]
min_x = np.min(x_values)
max_x = np.max(x_values)
min_y = np.min(y_values)
max_y = np.max(y_values)

# Calculate the width and height of the bounding box
width = max_x - min_x
height = max_y - min_y

# Print the length and width of the entire grid
print("Length of the Entire Grid:", width)
print("Width of the Entire Grid:", height)


# Create a scatter plot to visualize the detected hole positions
plt.figure(figsize=(8, 6))
plt.scatter(detected_holes_array[:, 0], detected_holes_array[:, 1], c='red', marker='o', s=10)
plt.title('Detected Holes')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.gca().invert_yaxis()  # Invert the y-axis to match image coordinates (0,0 at top-left)
plt.grid(True)
plt.show()

