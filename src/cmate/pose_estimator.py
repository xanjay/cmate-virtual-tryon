"""
pose estimator for extrating shoulder location.
"""
import cv2 as cv
import math


protoFile = "E:\\Sanjay\\mlprojects\\semantic_segmentation\\pose_estimation\\mpii_model\\pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "E:\\Sanjay\\mlprojects\\semantic_segmentation\\pose_estimation\\mpii_model\\pose_iter_160000.caffemodel"

THRESHOLD = 0.3
HEIGHT = 368
WIDTH = 368
SCALE = 0.003922

BODY_PARTS = {"Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
              "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
              "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14,
              "Background": 15}

POSE_PAIRS = [["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
              ["RElbow", "RWrist"], ["Neck", "LShoulder"], [
                  "LShoulder", "LElbow"],
              ["LElbow", "LWrist"], ["Neck", "Chest"], [
                  "Chest", "RHip"], ["RHip", "RKnee"],
              ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"]]


def find_rotation_angle(a,b):
    """
    find angle a of right angled traingle with ab as hypotenous
    <)bac
    """
    try:
        c = (b[0],a[1])
        ratio = (c[1]-b[1])/(c[0]-a[0])
        # print("ratio",ratio)
        angle = math.degrees(math.atan(ratio))
        return angle
    except ZeroDivisionError:
        raise Exception("left shoulder and right shoulder detected at same location.")

class PoseEstimator:
    def __init__(self, frame, origin="source"):
        """
        Initialize estimator
        frame: image array
        """
        self.origin = origin
        self.frame = frame
        self.net = cv.dnn.readNet(cv.samples.findFile(protoFile),
                                  cv.samples.findFile(weightsFile))
        self.shoulder_points = self.get_shoulder_loc()
    
    def get_shoulder_loc(self):
        """
        return shoulder locations.
        """
        frameWidth = self.frame.shape[1]
        frameHeight = self.frame.shape[0]
        inp = cv.dnn.blobFromImage(self.frame, SCALE, (WIDTH, HEIGHT),
                                  (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(inp)
        out = self.net.forward()

        assert(len(BODY_PARTS) <= out.shape[1])

        # find right and left shoulder
        shoulder_points = []
        for i in [2, 5]:
            # Slice heatmap of corresponding body's part.
            heatMap = out[0, i, :, :]

            _, conf, _, point = cv.minMaxLoc(heatMap)  # (min, max, minloc, maxloc)
            x = (frameWidth * point[0]) / out.shape[3]
            y = (frameHeight * point[1]) / out.shape[2]

            # Add a point if it's confidence is higher than threshold.
            if conf > THRESHOLD:
               shoulder_points.append((int(x), int(y)))

        print("Shoulder Points:", shoulder_points)
        return shoulder_points

    def get_shoulder_details(self):
        # step 3: get shoulder width and rotation angle
        # raises: shoulder not found.
        if len(self.shoulder_points)<2:
            # print(self.origin+" image w/o shoulder.")
            raise Exception(self.origin+" image without shoulder.")

        distance = self.shoulder_points[1][0] - self.shoulder_points[0][0]
        rotation_angle = find_rotation_angle(self.shoulder_points[0], self.shoulder_points[1])

        return distance, rotation_angle

