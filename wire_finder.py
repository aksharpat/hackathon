import cv2
import numpy as np
import matplotlib.pyplot as plt

green_object_boxes = []
# Load the image
image = cv2.imread("temp/cropped_object_0.jpg")

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
        box[:, 0] -= 50  # Adjust left (x-coordinate)
        box[:, 1] -= 10  # Adjust up (y-coordinate)

        # Add the adjusted bounding box to the green_object_boxes list
        green_object_boxes.append(box)

green_object_lines = []

for box in green_object_boxes:
    # Calculate the midpoint of the bounding box
    mid_x = np.mean(box[:, 0])
    mid_y = np.mean(box[:, 1])

    # Calculate the direction of the diagonal line
    dx = box[2][0] - box[0][0]
    dy = box[2][1] - box[0][1]

    # Normalize the direction vector
    length = np.sqrt(dx**2 + dy**2)
    dx /= length
    dy /= length

    # Calculate the starting and ending points for the line along the middle of the box
    line_length = (
        min(np.linalg.norm(box[0] - box[2]), np.linalg.norm(box[1] - box[3])) / 2
    )
    x1 = mid_x - dx * line_length
    y1 = mid_y - dy * line_length
    x2 = mid_x + dx * line_length
    y2 = mid_y + dy * line_length

    # Append the start and end points as a pair to the green_object_lines list
    green_object_lines.append([(x1, y1), (x2, y2)])

# Convert the green_object_lines list to a NumPy array
green_object_lines = np.array(green_object_lines)


green_objects = [
    contour for contour in contours if cv2.contourArea(contour) > min_contour_area
]

i = 0
# Draw rotated rectangles around detected green objects on the original image
for contour in green_objects:
    # Find the minimum area rotated rectangle
    rect = cv2.minAreaRect(contour)

    # Convert rectangle parameters to integers
    box = np.int0(cv2.boxPoints(rect))

    # Draw the rotated rectangle on the original image
    cv2.drawContours(image, [box], 0, (0, 255, 0), 4)

    # Label the bounding box with "wire" (larger font size)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (box[0][0] - 1000, box[0][1] - 130)  # Adjust the position for the label
    font_scale = 3.0  # Increase the font size further
    font_color = (0, 0, 255)  # Green color
    font_thickness = 13  # Increase the font thickness for better visibility
    temp_coord = green_object_lines[i]
    pt1, pt2 = temp_coord  # Get the start and end points of the line

    pt1 = (int(round(pt1[0])), int(round(pt1[1])))
    pt2 = (int(round(pt2[0])), int(round(pt2[1])))
    temp_coord = (pt1, pt2)
    cv2.putText(
        image,
        f"wire {temp_coord}",
        org,
        font,
        font_scale,
        font_color,
        font_thickness,
    )
    i += 1

# Display the result
cv2.imwrite("wires_labeled_large_font.jpg", image)
cv2.imshow("Green Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
