import cv2
import numpy as np

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# define bounds of red
lower_red1 = np.array([0, 120, 120])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 120])
upper_red2 = np.array([180, 255, 255])

# take frame
ret, frame = cap.read()
# write frame to file
cv2.imwrite('LaserPath/TestImages/lsrdImage.jpg', frame)
# release camera
cap.release()