import os
import cv2 as cv


import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pose_estimator import PoseEstimator

image_loc = "C:\\Users\\sanja\\Desktop\\photo-smiling-woman-standing-up.jpg"
img = cv.imread(image_loc)
shoulder_points = PoseEstimator(img, "dest").shoulder_points

# draw ellipse
cv.ellipse(img, shoulder_points[0], (3, 3),
           0, 0, 360, (0, 255, 0), cv.FILLED)
cv.ellipse(img, shoulder_points[1], (3, 3),
           0, 0, 360, (0, 0, 255), cv.FILLED)
cv.imshow("destination", img)

cv.waitKey(0)
