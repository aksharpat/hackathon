import cv2 as cv
import numpy as np


def process_image(image_path):
    # Load the image
    image = cv.imread(image_path)

    # Crop the image
    cropped_image = crop_image(image)

    # Cleans/sharpens the image
    cleaned_image = clean_image(cropped_image)

    # TODO: Replace this with cleaned_image. Use cropped_image for testing
    cv.imshow(cropped_image)


def crop_image(image):
    """
    Crops the image.
    Input: Imread Mat object.
    Output: Cropped image.
    """
    ###

    # Load the image
    image = cv.imread("thomp2.jpg")

    # Convert the image to grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Apply a binary threshold or any other suitable preprocessing
    _, thresh = cv.threshold(gray, 128, 255, cv.THRESH_BINARY)

    # Find contours in the binary image
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Initialize a list to store cropped objects
    cropped_objects = []

    # Set minimum contour area and aspect ratio thresholds
    min_contour_area = 1000  # Adjust this value as needed
    min_aspect_ratio = 0.3  # Adjust this value as needed

    # Iterate through the detected contours
    for contour in contours:
        # Calculate the contour area
        contour_area = cv.contourArea(contour)

        # Calculate the bounding rectangle for the contour
        x, y, w, h = cv.boundingRect(contour)

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
        # cv.imshow(f"Cropped Object {i}", cropped_object)
        cv.imwrite(f"cropped_object_{i}.jpg", cropped_object)

    # Display the original image with rectangles (optional)
    for contour in contours:
        x, y, w, h = cv.boundingRect(contour)
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv.imshow("Object Detection", image)
    cv.waitKey(0)
    cv.destroyAllWindows()
    ###


def clean_image(image):
    """
    Cleans/processes the image.
    Input: Cropped Imread Mat object.
    Output: Cleaned image.
    """
    # TODO: Ethan put code here
    pass


if __name__ == "__main__":
    image_path = "breadboard.jpg"
    process_image(image_path)
