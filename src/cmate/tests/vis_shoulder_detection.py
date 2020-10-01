import os
import cv2 as cv


import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from pose_estimator import PoseEstimator

# test run
SAMPLES_DIR = os.environ['ROOT_DIR']+"/src/flask_app/static/images/samples"
sample_file = SAMPLES_DIR+"/profile_images/sample-profile-image1.jpg"

img = cv.imread(sample_file)
PoseEstimator(img).visualize_pose()
