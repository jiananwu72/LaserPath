import cv2
import numpy as np

# Load the image
image = cv2.imread('LaserPath/TestImages/lsrdImage.jpg')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define lower and upper ranges for the red color in HSV.
lower_red1 = np.array([0, 100, 100])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([160, 100, 100])
upper_red2 = np.array([179, 255, 255])
mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)

# Clean up the mask using morphological operations
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    largest_contour = max(contours, key=cv2.contourArea)
    M = cv2.moments(largest_contour)
    if M["m00"] != 0:
        centerX = int(M["m10"] / M["m00"])
        centerY = int(M["m01"] / M["m00"])
    else:
        centerX, centerY = 0, 0

    cv2.circle(image, (centerX, centerY), 10, (0, 255, 0), -1)  # Green circle
    x, y, w, h = cv2.boundingRect(largest_contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle

    label_text = f"Laser: ({centerX}, {centerY})"
    cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
else:
    print("No red laser beam detected.")

cv2.imwrite("output_image.jpg", image)
# cv2.imshow("Detected Laser", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
