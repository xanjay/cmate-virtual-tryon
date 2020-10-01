"""
pose estimator for extrating shoulder location.
"""
import cv2 as cv
import math
import os

# choose one of "mpi" or "body_24" openpose model 
model = "body_25"
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "segmentation", "models")

if model == "mpi":
    protoFile = os.path.join(MODEL_DIR, "pose_deploy_linevec.prototxt")
    weightsFile = os.path.join(MODEL_DIR, "pose_iter_160000.caffemodel")
    THRESHOLD = 0.3
else:
    protoFile = os.path.join(MODEL_DIR, "mpii_openpose_body25", "pose_deploy.prototxt")
    weightsFile = os.path.join(MODEL_DIR, "mpii_openpose_body25", "pose_iter_584000.caffemodel")
    THRESHOLD = 0.1

HEIGHT = 368
WIDTH = 368
SCALE = 0.003922  # 1.0/255

# body parts ordering
# https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md#keypoint-ordering-in-cpython
BODY_PARTS = {"RShoulder": 2, "LShoulder": 5}


def find_rotation_angle(a, b):
    """
    find angle a of right angled traingle with ab as hypotenous
    <)bac
    """
    try:
        c = (b[0], a[1])
        ratio = (c[1]-b[1])/(c[0]-a[0])
        # print("ratio",ratio)
        angle = math.degrees(math.atan(ratio))
        return angle
    except ZeroDivisionError:
        raise Exception("left shoulder and right shoulder detected at same location.")


class PoseEstimator:
    def __init__(self, frame):
        """
        Initialize estimator
        frame: image array
        """
        self.frame = frame
        self.net = cv.dnn.readNetFromCaffe(protoFile, weightsFile)
        self.shoulder_points = []

    def get_shoulder_points(self):
        """
        return shoulder locations.
        """
        if len(self.shoulder_points) > 0:
            return self.shoulder_points

        frameWidth = self.frame.shape[1]
        frameHeight = self.frame.shape[0]
        inp = cv.dnn.blobFromImage(self.frame, SCALE, (WIDTH, HEIGHT),
                                   (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(inp)
        self.out = self.net.forward()
        # print(self.out.shape)

        assert(len(BODY_PARTS) <= self.out.shape[1])

        # find right and left shoulder
        shoulder_points = []
        for i in [2, 5]:
            # Slice heatmap of corresponding body's part.
            heatMap = self.out[0, i, :, :]

            _, conf, _, point = cv.minMaxLoc(
                heatMap)  # (min, max, minloc, maxloc)
            x = (frameWidth * point[0]) / self.out.shape[3]
            y = (frameHeight * point[1]) / self.out.shape[2]

            # Add a point if it's confidence is higher than threshold.
            if conf > THRESHOLD:
                shoulder_points.append((int(x), int(y)))

        print("Shoulder Points:", shoulder_points)
        return shoulder_points

    def get_shoulder_details(self):
        # get shoulder points
        self.shoulder_points = self.get_shoulder_points()
        # step 3: get shoulder width and rotation angle
        # raises: shoulder not found.
        if len(self.shoulder_points) < 2:
            raise Exception("image without shoulder.")

        distance = self.shoulder_points[1][0] - self.shoulder_points[0][0]
        # rotation_angle = find_rotation_angle(self.shoulder_points[0], self.shoulder_points[1])

        return distance

    def visualize_pose(self):
        try:
            self.shoulder_points = self.get_shoulder_points()
            
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10,5))
            # draw points
            plt.subplot(1,2,1)
            cv.ellipse(self.frame, tuple(self.shoulder_points[0]),
                       (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)
            cv.ellipse(self.frame, tuple(self.shoulder_points[1]),
                       (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            plt.imshow(cv.cvtColor(self.frame, cv.COLOR_BGR2RGB))
            # draw heatmaps
            plt.subplot(1, 2, 2)
            plt.imshow(cv.cvtColor(self.frame, cv.COLOR_BGR2RGB))          
            for pt in [2, 5]:
                probMap = self.out[0, pt, :, :]
                probMap = cv.resize(probMap,(self.frame.shape[1], self.frame.shape[0]))
                
                plt.imshow(probMap, alpha=0.6)
            plt.colorbar()
            plt.axis("off")
            plt.show()
        except IndexError:
            raise Exception("Shoulder not detected.")

