import cv2
import numpy as np

image = cv2.imread("breadboard.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(
    gray, threshold1=30, threshold2=100
)  # Adjust the thresholds as needed
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

mask = np.zeros_like(gray)
cv2.drawContours(mask, [largest_contour], 0, (255), thickness=cv2.FILLED)

breadboard_only = cv2.bitwise_and(image, image, mask=mask)

cv2.imwrite("cropped_breadboard.jpg", breadboard_only)
