import cv2
import numpy as np

# Load the image
image = cv2.imread('breadboard3.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Minimum and maximum area for a hole (you may need to adjust these values)
min_hole_area = 50
max_hole_area = 2000

# Loop through the contours
for contour in contours:
    # Calculate the area of the contour
    area = cv2.contourArea(contour)
    
    if min_hole_area < area < max_hole_area:
        # Draw the contour on the original image (optional)
        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        
        # Get the coordinates of the center of the hole
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Draw a circle at the center of the hole
            cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

# Save the processed image as a JPEG
cv2.imwrite('breadboard_processed.jpg', image)

# Display the original image with contours and centers
cv2.imshow("Breadboard Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
