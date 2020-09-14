import os
import cv2 as cv


import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pose_estimator import PoseEstimator

sample_file = "E:\\Sanjay\\mlprojects\\virtual_try_on\\src\\flask_app\\files\\user_uploads\\n00554A.jpg"
img = cv.imread(sample_file)
PoseEstimator(img).visualize_pose()
