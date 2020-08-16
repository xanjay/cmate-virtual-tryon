"""
module to locate shoulder details mannually in cloth 
"""

from pose_estimator import find_rotation_angle
import cv2 as cv
import utils
import numpy as np


def get_shoulder_loc_mannual(cloth_seg):
    "mannually locate shoulder points"

    # crop cloth segmentation
    start_crop, crop_seg = utils.crop_square(cloth_seg)
    crop_seg = cv.cvtColor(crop_seg, cv.COLOR_BGR2GRAY)
    height, width = crop_seg.shape[:2]
    # find right and left shoulder
    #  TODO: take 10% width offset
    offset = int(0.20*width)
    # print(offset)
    # right shoulder
    col_vector = crop_seg[:, offset]
    right_shoulder = (offset+start_crop[1], min(np.where(col_vector!=0)[0])+start_crop[0])
    # left shoulder
    col_vector = crop_seg[:, width-offset]
    left_shoulder = (width-offset+start_crop[1], min(np.where(col_vector!=0)[0]+start_crop[0]))

    shoulder_points = [right_shoulder, left_shoulder]
    print("Shoulder Points:",shoulder_points)

    return shoulder_points

def get_shoulder_details_mannual(cloth_seg):
    # get shoulder width and rotation angle
    shoulder_points = get_shoulder_loc_mannual(cloth_seg)

    distance = shoulder_points[1][0] - shoulder_points[0][0]
    rotation_angle = find_rotation_angle(shoulder_points[0], shoulder_points[1])

    return shoulder_points, distance, rotation_angle

# img = cv.imread("C:\\Users\\sanja\\Desktop\\testseg.jpg")
# print(get_shoulder_details_mannual(img))