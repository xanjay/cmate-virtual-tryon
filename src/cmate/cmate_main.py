from pose_estimator import PoseEstimator
import custom_shoulder_locator
from segmentation import cloth_extractor
import utils

import cv2 as cv
import imutils

#TODO: create error list
ERROR_LIST = [] # e.g. angle and distance too high

class CMate:
    def __init__(self, source_img, dest_img):
        self.source_img = source_img
        self.dest_img = dest_img
        self.dest_pose_estimator = PoseEstimator(
            cv.imread(self.dest_img), "dest")
        self.source_pose_estimator = None  # initialize after cloth extraction

    def cloth_segmentation(self):
        # extract source image and segmented cloth
        source_img, source_seg = cloth_extractor.extract_cloth(self.source_img)
        source_img = cv.cvtColor(source_img, cv.COLOR_RGB2BGR)
        source_seg = cv.cvtColor(source_seg, cv.COLOR_RGB2BGR)
        # print(source_img.shape, source_seg.shape)
        # fill holes
        source_seg = utils.fill_holes(source_img, source_seg)

        return source_img, source_seg

    def get_source_shoulder_details(self, source_img, cloth_seg):
        "get source shoulder distance and rotation angle"

        try:
            # initialize source pose estimator
            self.source_pose_estimator = PoseEstimator(source_img, "source")
            source_distance, source_angle = self.source_pose_estimator.get_shoulder_details()
            source_points = self.source_pose_estimator.shoulder_points
        except Exception as e:
            print(str(e))
            # if no source shoulder points detected
            source_points, source_distance, source_angle = custom_shoulder_locator.get_shoulder_details_mannual(cloth_seg)

        return source_points, source_distance, source_angle

    def apply_cloth(self):
        # step 1: get dest shoulder distance and rotation angle
        dest_distance, dest_angle = self.dest_pose_estimator.get_shoulder_details()

        # step 2: get source image and segmented cloth
        source_img, source_seg = self.cloth_segmentation()

        # cv.imwrite("C:\\Users\\sanja\\Desktop\\testseg.jpg", source_seg)

        # step 3: get source shoulder distance and rotation angle
        source_points, source_distance, source_angle = self.get_source_shoulder_details(
            source_img, source_seg)

        # step 4: resize source seg and shoulder points
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

        # step 5: rotate source seg and shoulder points
        rotation_angle = dest_angle - source_angle
        # clip angle between [-5,5]
        rotation_angle = max(-5, min(rotation_angle, 5))
        print("rotation angle:", rotation_angle)
        rotated_seg = imutils.rotate(source_seg, rotation_angle)
        source_points = utils.rotate_shoulder_points(source_seg, source_points,
                                                     rotation_angle)

        # step 5.2: remove border
        mask, rotated_seg = utils.remove_segmentation_border(rotated_seg, cv)

        # step 6: blend dest image and extracted cloth
        dest_frame = cv.imread(self.dest_img)
        dest_points = self.dest_pose_estimator.shoulder_points
        final_img = utils.blend_images(
            rotated_seg, source_points, dest_frame, dest_points)

        return final_img

    def visualize(self):
        # first apply cloth
        final_img = self.apply_cloth()
        cv.imshow("final img", final_img)

        source_frame = cv.imread(self.source_img)
        cv.imshow("source img", source_frame)

        dest_frame = cv.imread(self.dest_img)
        cv.imshow("dest img", dest_frame)

        cv.waitKey(0)
        cv.destroyAllWindows()

    def visualize_shoulder(self):
        # step 1: get dest shoulder distance and rotation angle
        dest_distance, dest_angle = self.dest_pose_estimator.get_shoulder_details()

        # step 2: get source image and segmented cloth
        source_img, source_seg = cloth_extractor.extract_cloth(self.source_img)
        source_img = cv.cvtColor(source_img, cv.COLOR_RGB2BGR)
        source_seg = cv.cvtColor(source_seg, cv.COLOR_RGB2BGR)
        print(source_img.shape, source_seg.shape)
        # step 2.2: fill holes
        source_seg = utils.fill_holes(source_img, source_seg)

        # initialize source pose estimator
        self.source_pose_estimator = PoseEstimator(source_img, "source")

        # step 3: get source shoulder distance and rotation angle
        source_distance, source_angle = self.source_pose_estimator.get_shoulder_details()

        # step 4: resize source seg and shoulder points
        resize_factor = dest_distance/source_distance
        print("resize factor:", resize_factor)

        source_seg = cv.resize(source_seg,
                               (int(source_seg.shape[1]*resize_factor),
                                int(source_seg.shape[0]*resize_factor))
                               )
        source_points = self.source_pose_estimator.shoulder_points
        source_points[0] = utils.resize_shoulder_coord(
            source_points[0], resize_factor)
        source_points[1] = utils.resize_shoulder_coord(
            source_points[1], resize_factor)

        # step 5: rotate source seg and shoulder points
        rotation_angle = dest_angle - source_angle
        rotated_seg = imutils.rotate(source_seg, rotation_angle)
        source_points = utils.rotate_shoulder_points(source_seg, source_points,
                                                     rotation_angle)

        # print("Rotated:", source_points)

        # step 5.2: remove border
        mask, clean_seg = utils.remove_segmentation_border(rotated_seg)

        # step 6: visualize
        source_frame = clean_seg

        cv.ellipse(source_frame, tuple(source_points[0]),
                   (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)
        cv.ellipse(source_frame, tuple(source_points[1]),
                   (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

        source_frame[np.where(mask != 200)] = 255
        cv.imshow("source", source_frame)

        dest_frame = cv.imread(self.dest_img)
        dest_points = self.dest_pose_estimator.shoulder_points

        cv.ellipse(dest_frame, dest_points[0], (3, 3),
                   0, 0, 360, (0, 255, 0), cv.FILLED)
        cv.ellipse(dest_frame, dest_points[1], (3, 3),
                   0, 0, 360, (0, 0, 255), cv.FILLED)
        cv.imshow("destination", dest_frame)

        # cv.imshow("final", final_img)

        cv.waitKey(0)
        cv.destroyAllWindows()


# test run
# SOURCE_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\vest.jpg"
# DEST_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\figure-above.jpg"

# SOURCE_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\selena.jpg"
# DEST_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\figure-above.jpg"

# cloth_blender = CMate(SOURCE_IMG, DEST_IMG)
# cloth_blender.visualize()

