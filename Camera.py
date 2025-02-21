import cv2
import numpy as np

# open camera
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# take frame
ret, frame = cap.read()
# write frame to file
cv2.imwrite('LaserPath/RawImages/MP2.jpg', frame)
# release camera
cap.release()