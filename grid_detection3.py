import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle
from scipy.spatial import KDTree

Y_THRESH = 25  # Threshold distance to determine if two holes belong to the same row
# TODO: better way of doing this.


def non_max_suppression(rectangles, min_distance):
    if len(rectangles) == 0:
        return []

    rectangles = np.array(rectangles)
    rectangles = rectangles[np.argsort(rectangles[:, 0])]
    picked_rectangles = [rectangles[0]]

    for rect in rectangles[1:]:
        distances = np.sqrt(np.sum(np.square(picked_rectangles - rect), axis=1))
        if np.min(distances) >= min_distance:
            picked_rectangles.append(rect)

    return picked_rectangles


def adjust_rows(rows):
    adjusted_rows = []

    for row in rows:
        sorted_row = sorted(row, key=lambda x: x[0])
        quarter_length = len(sorted_row) // 4
        middle_section = sorted_row[quarter_length:-quarter_length]
        avg_y = np.mean([pt[1] for pt in middle_section])
        adjusted_row = [(pt[0], int(avg_y)) for pt in sorted_row]
        adjusted_rows.extend(adjusted_row)

    return adjusted_rows


# Load the breadboard image
breadboard_image = cv2.imread("imgs/breadboard10.jpg")

# Create a list of template images
template_paths = [
    "resources/template10.jpg",
    "resources/template11.jpg",
    "resources/template14.jpg",
    "resources/template15.jpg",
    "resources/template16.jpg",
    "resources/template17.jpg",
    "resources/template20.jpg",
    "resources/template21.jpg",
]  # Add paths to your templates

# Set a threshold to determine matching locations
threshold = 0.77  # Adjust this threshold as needed
min_distance = 50
detected_holes_positions = []

for template_path in template_paths:
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(breadboard_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        detected_holes_positions.append(pt)

detected_holes_positions = non_max_suppression(
    detected_holes_positions, min_distance=min_distance
)

sorted_holes = sorted(detected_holes_positions, key=lambda x: x[1])
rows = []
current_row = [sorted_holes[0]]

for i in range(1, len(sorted_holes)):
    if abs(sorted_holes[i][1] - sorted_holes[i - 1][1]) < Y_THRESH:
        current_row.append(sorted_holes[i])
    else:
        rows.append(current_row)
        current_row = [sorted_holes[i]]
rows.append(current_row)

adjusted_holes = adjust_rows(rows)
detected_holes_array = np.array(adjusted_holes)

x_values = detected_holes_array[:, 0]
y_values = detected_holes_array[:, 1]
min_x = np.min(x_values)
max_x = np.max(x_values)
min_y = np.min(y_values)
max_y = np.max(y_values)

width = max_x - min_x
height = max_y - min_y

with open("resources/holemap_small.pkl", "rb") as file:
    neat_array = pickle.load(file)


# Calculate the aspect ratio of neat_array
neat_aspect_ratio = (
    width / height
)  # Assuming width and height are the dimensions of neat_array

# Calculate the aspect ratio of detected_holes_array
detected_aspect_ratio = (max_x - min_x) / (max_y - min_y)
# Determine the scaling factor based on aspect ratios
if detected_aspect_ratio < neat_aspect_ratio:
    # detected_holes_array is narrower, scale its height to match neat_array
    scale_factor = (max_x - min_x) / width
else:
    # detected_holes_array is wider, scale its width to match neat_array
    scale_factor = (max_y - min_y) / height

# Calculate the dimensions of the scaled detected holes array
scaled_width = max_x - min_x
scaled_height = max_y - min_y

# Print the dimensions of both arrays
print("Dimensions of Neat Array (width x height):", width, "x", height)
print(
    "Dimensions of Scaled Detected Holes Array (width x height):",
    scaled_width,
    "x",
    scaled_height,
)

# Scale the coordinates of detected_holes_array
scaled_detected_holes_array = detected_holes_array * 0.95
print(scale_factor)
# Calculate the centroid of both arrays
neat_centroid = np.mean(neat_array, axis=0)
detected_holes_centroid = np.mean(scaled_detected_holes_array, axis=0)

# Calculate the offset needed to align the centroids
offset = neat_centroid - detected_holes_centroid

# Shift the scaled_detected_holes_array by the calculated offset
aligned_scaled_detected_holes_array = scaled_detected_holes_array + offset
print(offset)

# ---------- KDTree Grid Shifting --------------

# Create a KDTree from the neat array
tree = KDTree(neat_array)

# For each point in the aligned_scaled_detected_holes_array,
# find the nearest neighbor in the neat_array
dists, idxs = tree.query(aligned_scaled_detected_holes_array)

# Compute the shifts required to align each point from
# aligned_scaled_detected_holes_array to its nearest neighbor
shifts = neat_array[idxs] - aligned_scaled_detected_holes_array

# Apply the shifts to the points in aligned_scaled_detected_holes_array
aligned_scaled_detected_holes_array += shifts

# ----------------------------------------------

# Create a scatter plot to visualize the aligned arrays
plt.figure(figsize=(8, 6))
plt.scatter(
    aligned_scaled_detected_holes_array[:, 0],
    aligned_scaled_detected_holes_array[:, 1],
    c="red",
    marker="o",
    s=10,
    label="Aligned Detected Holes",
)
plt.scatter(
    neat_array[:, 0], neat_array[:, 1], c="blue", marker="x", s=10, label="Neat Array"
)
plt.title("Aligned Detected Holes and Neat Array")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.gca().invert_yaxis()
plt.grid(True)
plt.legend()
plt.show()
