import cv2 as cv
import numpy as np


def process_image(image_path):
    # Load the image
    image = cv.imread(image_path)

    # Crop the image
    cropped_image = crop_image(image)

    # Cleans/sharpens the image
    cleaned_image = clean_image(image)

    # TODO: Replace this with cleaned_image. Use cropped_image for testing
    cv.imshow(cropped_image)


def crop_image(image):
    """
    Crops the image.
    Input: Imread Mat object.
    Output: Cropped image.
    """
    ###
    # TODO: Akshar put code here
    ###
    pass


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
