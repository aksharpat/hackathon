import cv2

# Load the breadboard image
image = cv2.imread('breadboard2.jpg')

# Check if the image was loaded successfully
if image is None:
    print("Error: Could not load the image.")
else:
    max_width = 800
    height, width, _ = image.shape

    if width > max_width:
        ratio = max_width / width
        new_height = int(height * ratio)
        image = cv2.resize(image, (max_width, new_height))
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding to create a binary image
    _, binary_image = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY)

    # Apply edge detection
    edges = cv2.Canny(binary_image, 100, 200)  # Adjust the thresholds as needed

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Define minimum contour area and aspect ratio for filtering
    min_contour_area = 10  # Adjust this value as needed
    min_aspect_ratio = 0.3  # Adjust as per your components
    max_aspect_ratio = 2.5  # Adjust as per your components

    # Draw bounding boxes around detected components
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        if cv2.contourArea(contour) > min_contour_area and min_aspect_ratio <= aspect_ratio <= max_aspect_ratio:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw a green rectangle

    # Display the result (you can save it using cv2.imwrite() as well)
    cv2.imshow('Breadboard Components', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
