from pose_estimator import PoseEstimator
import custom_shoulder_locator
from segmentation import cloth_extractor
import utils

import cv2 as cv
import imutils
import logging

#TODO: create error list
ERROR_LIST = [] # e.g. shoulder detection error
MIN_SHOULDER_DISTANCE=0

class CMate:
    def __init__(self, source_img, dest_img):
        self.source_img = source_img
        self.dest_img = dest_img
        self.dest_pose_estimator = PoseEstimator(cv.imread(self.dest_img))
        self.source_pose_estimator = None  # initialize after cloth extraction
        self.error_list = []

    def cloth_segmentation(self):
        # extract source image and segmented cloth
        try:
            source_img, source_seg = cloth_extractor.extract_cloth(self.source_img)
        
            source_img = cv.cvtColor(source_img, cv.COLOR_RGB2BGR)
            source_seg = cv.cvtColor(source_seg, cv.COLOR_RGB2BGR)
            # print(source_img.shape, source_seg.shape)
            # fill holes
            source_seg = utils.fill_holes(source_img, source_seg)

            return source_img, source_seg
        except Exception:
            raise Exception("Source image without cloth.")

    def get_source_shoulder_details(self, source_img, cloth_seg):
        "get source shoulder distance and rotation angle"

        try:
            # initialize source pose estimator
            self.source_pose_estimator = PoseEstimator(source_img)
            source_distance = self.source_pose_estimator.get_shoulder_details()
            source_points = self.source_pose_estimator.get_shoulder_points()
        except Exception as e:
            print(str(e))
            # if no source shoulder points detected
            self.error_list.append("Issue in source image:"+str(e))
            logging.warning("Using manual shoulder detection for source image.")
            source_points, source_distance = custom_shoulder_locator.get_shoulder_details_mannual(cloth_seg)

        return source_points, source_distance

    def apply_cloth(self):
        # step 1: get dest shoulder distance and rotation angle
        try:
            dest_distance = self.dest_pose_estimator.get_shoulder_details()
        except Exception as e:
            raise Exception("Issue in profile image:"+str(e))
        # step 2: get source image and segmented cloth
        source_img, source_seg = self.cloth_segmentation()

        # cv.imwrite("testseg.jpg", source_seg)

        # step 3: get source shoulder distance and rotation angle
        source_points, source_distance = self.get_source_shoulder_details(
            source_img, source_seg)

        # step 4: resize source seg and shoulder points
        if dest_distance < MIN_SHOULDER_DISTANCE:
            raise Exception("Shoulder detection issue in profile image.")
        if source_distance < MIN_SHOULDER_DISTANCE:
            raise Exception("Shoulder detection issue in source image.")
        resize_factor = dest_distance/source_distance
        print("resize factor:", resize_factor)

        source_seg = cv.resize(source_seg,
                               (int(source_seg.shape[1]*resize_factor),
                                int(source_seg.shape[0]*resize_factor))
                               )

        source_points[0] = utils.resize_shoulder_coord(
            source_points[0], resize_factor)
        source_points[1] = utils.resize_shoulder_coord(
            source_points[1], resize_factor)
        """
        # step 5: rotate source seg and shoulder points
        rotation_angle = dest_angle - source_angle
        # clip angle between [-10,10]
        if abs(rotation_angle) > 5:
            self.error_list.append("Source Image is rotated: %f" % rotation_angle)
        rotation_angle = max(-10, min(rotation_angle, 10))
        print("rotation angle:", rotation_angle)
        rotated_seg = imutils.rotate(source_seg, rotation_angle)
        source_points = utils.rotate_shoulder_points(source_seg, source_points,
                                                     rotation_angle)
        """

        # step 5.2: remove border
        _, source_seg = utils.remove_segmentation_border(source_seg)

        # step 6: blend dest image and extracted cloth
        dest_frame = cv.imread(self.dest_img)
        dest_points = self.dest_pose_estimator.get_shoulder_points()
        try:
            final_img = utils.blend_images(
                source_seg, source_points, dest_frame, dest_points)
        except AssertionError:
            print("Assertion Error in blending images.")
            raise Exception("Issue in blending Images.")
        except Exception as e:
            print(str(e))
            raise Exception("Issue in blending Images.")
        return final_img, self.error_list


