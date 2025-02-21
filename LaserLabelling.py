import cv2
import numpy as np

# Load the image
image = cv2.imread('LaserPath/RawImages/FE1.jpg')

# Convert the image from BGR to HSV/HLS color space
cvtImage = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
# cvtImage = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define Red Color Ranges and Create a Mask
lower_red1 = np.array([0, 240, 0])
upper_red1 = np.array([180, 255, 150])
lower_red2 = np.array([0, 230, 200])
upper_red2 = np.array([180, 255, 255])
mask1 = cv2.inRange(cvtImage, lower_red1, upper_red1)
mask2 = cv2.inRange(cvtImage, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
cv2.imwrite("LaserPath/ProcessedImages/FE1/mask1.jpg", mask1)
cv2.imwrite("LaserPath/ProcessedImages/FE1/mask2.jpg", mask2)
cv2.imwrite("LaserPath/ProcessedImages/FE1/mask.jpg", mask)

# Denoise the mask using morphological operations
# kernel = np.ones((5, 5), np.uint8)
kernel = np.array([[0.5, 1, 0.5], [1, 2, 1], [0.5, 1, 0.5]])
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
cv2.imwrite("LaserPath/ProcessedImages/FE1/maskDenoised.jpg", mask)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
if contours:
    # largest_contour = max(contours, key=cv2.contourArea)
    # M = cv2.moments(largest_contour)
    # if M["m00"] != 0:
    #     centerX = int(M["m10"] / M["m00"])
    #     centerY = int(M["m01"] / M["m00"])
    # else:
    #     centerX, centerY = 0, 0

    # # cv2.circle(image, (centerX, centerY), 10, (0, 255, 0), -1)  # Green circle
    # cv2.drawContours(image, [largest_contour], -1, (0, 0, 255), 2)  # Red contour
    # x, y, w, h = cv2.boundingRect(largest_contour)
    # cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle
    # label_text = f"Laser: ({centerX}, {centerY})"
    # cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    print("Number of contours:", len(contours))
    for c in contours:
        # M = cv2.moments(c)
        # if M["m00"] != 0:
        #     centerX = int(M["m10"] / M["m00"])
        #     centerY = int(M["m01"] / M["m00"])
        # else:
        #     centerX, centerY = 0, 0
        # cv2.circle(image, (centerX, centerY), 10, (0, 255, 0), -1)  # Green circle
        
        cv2.drawContours(image, [c], -1, (0, 0, 255), 2)  # Red contour
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Blue rectangle
        # label_text = f"Laser: ({centerX}, {centerY})"
        # cv2.putText(image, label_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

else:
    print("No red laser beam detected.")

cv2.imwrite("LaserPath/ProcessedImages/FE1/ContourLabel.jpg", image)

# Optionally, display the result in a window (press any key to close)
# cv2.imshow("Detected Laser", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
