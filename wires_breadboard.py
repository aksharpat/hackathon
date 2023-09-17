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
breadboard_image = cv2.imread("cropped_object_0.jpg")

# Create a list of template images
template_paths = [
    "template10.jpg",
    "template11.jpg",
    "template12.jpg",
    "template13.jpg",
    "template14.jpg",
    "template15.jpg",
    "template16.jpg",
    "template17.jpg",
    "template18.jpg",
    "template19.jpg",
]  # Add paths to your templates

# Set a threshold to determine matching locations
threshold = 0.77  # Adjust this threshold as needed
min_distance = 50  # Minimum distance between detected holes

# Initialize empty lists to store detected hole positions and green object bounding boxes
detected_holes_positions = []
green_object_boxes = []

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

# Apply non-maximum suppression to remove overlapping detections for holes
detected_holes_positions = non_max_suppression(
    detected_holes_positions, min_distance=min_distance
)

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
for contour in contours:
    if cv2.contourArea(contour) > min_contour_area:
        # Find the minimum area rotated rectangle
        rect = cv2.minAreaRect(contour)

        # Get the corner points of the rotated rectangle
        box = cv2.boxPoints(rect)

        # Convert the coordinates to integers and adjust them
        box = np.int0(box)
        box[:, 0] -= 10  # Adjust left (x-coordinate)
        box[:, 1] -= 10  # Adjust up (y-coordinate)

        # Add the adjusted bounding box to the green_object_boxes list
        green_object_boxes.append(box)

# Create a scatter plot to visualize the detected holes and green objects with bounding boxes
plt.figure(figsize=(8, 6))
for coordinates in detected_holes_positions:
    plt.scatter(coordinates[0], coordinates[1], c="red", marker="o", s=10)

for box in green_object_boxes:
    poly = plt.Polygon(box, closed=True, fill=None, edgecolor="g", linestyle="--")
    plt.gca().add_patch(poly)

plt.title("Detected Holes and Green Objects with Bounding Boxes")
plt.xlabel("X-coordinate")
plt.ylabel("Y-coordinate")
plt.gca().invert_yaxis()  # Invert the y-axis to match image coordinates (0,0 at top-left)
plt.grid(True)
plt.show()
