import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

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


breadboard_image = cv2.imread("imgs/breadboard7.jpg")
template_paths = [
    "resources/template10.jpg",
    "resources/template11.jpg",
    "resources/template12.jpg",
    "resources/template13.jpg",
    "resources/template14.jpg",
    "resources/template15.jpg",
    "resources/template16.jpg",
    "resources/template17.jpg",
    "resources/template18.jpg",
    "resources/template19.jpg",
]

threshold = 0.77
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

print("Length of the Entire Grid:", width)
print("Width of the Entire Grid:", height)

plt.figure(figsize=(8, 6))
plt.scatter(
    detected_holes_array[:, 0], detected_holes_array[:, 1], c="red", marker="o", s=10
)
plt.title("Detected Holes")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.gca().invert_yaxis()
plt.grid(True)
plt.show()

# Save detected_holes_array into a pickle file
with open("resources/holemap_small.pkl", "wb") as file:
    pickle.dump(detected_holes_array, file)
