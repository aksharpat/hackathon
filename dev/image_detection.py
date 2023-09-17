import cv2

# Load the image
image = cv2.imread("imgs/breadboard10.jpg")

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply a binary threshold or any other suitable preprocessing
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

# Find contours in the binary image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize a list to store cropped objects
cropped_objects = []

# Set minimum contour area and aspect ratio thresholds
min_contour_area = 1000  # Adjust this value as needed
min_aspect_ratio = 0.3  # Adjust this value as needed

# Iterate through the detected contours
for contour in contours:
    # Calculate the contour area
    contour_area = cv2.contourArea(contour)

    # Calculate the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Calculate the aspect ratio of the bounding rectangle
    aspect_ratio = float(w) / h

    # Filter contours based on area and aspect ratio
    if contour_area > min_contour_area and aspect_ratio > min_aspect_ratio:
        # Crop the object from the original image
        cropped_object = image[y : y + h, x : x + w]

        # Append the cropped object to the list
        cropped_objects.append(cropped_object)

# Display or save the cropped objects
for i, cropped_object in enumerate(cropped_objects):
    # cv2.imshow(f"Cropped Object {i}", cropped_object)
    cv2.imwrite(f"temp/cropped_object_{i}.jpg", cropped_object)

# Display the original image with rectangles (optional)
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Object Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
