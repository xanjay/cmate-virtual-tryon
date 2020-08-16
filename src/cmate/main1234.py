# To use Inference Engine backend, specify location of plugins:
# source /opt/intel/computer_vision_sdk/bin/setupvars.sh
import cv2 as cv
import numpy as np
import argparse
import os
import imutils
import math

from segmentation.cloth_extractor import extract_cloth



protoFile = "E:\\Sanjay\\mlprojects\\semantic_segmentation\\pose_estimation\\mpii_model\\pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "E:\\Sanjay\\mlprojects\\semantic_segmentation\\pose_estimation\\mpii_model\\pose_iter_160000.caffemodel"

# TEST_IMAGES = ["C:\\Users\\sanja\\Desktop\\pose_test\\"+item for item in os.listdir("C:\\Users\\sanja\\Desktop\\pose_test")]
# TEST_IMAGES[0] = "C:\\Users\\sanja\\Desktop\\test12345n.jpg"
SOURCE_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\vest.jpg"
DEST_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\figure-above.jpg"

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

def resize_image(image):
    max = max(image.shape[0], image.shape[1])
    image = cv.resize(image, (image.shape[0]*500/max, image.shape[1]*500/max))
    return image


def resize_shoulder_coord(loc, factor):
    return (int(loc[0]*factor), int(loc[1]*factor))

def find_rotation_angle(a,b):
    """
    find angle a of right angled traingle with ab as hypotenous
    <)bac
    """
    try:
        c = (b[0],a[1])
        ratio = (c[1]-b[1])/(c[0]-a[0])
        print("ratio",ratio)
        angle = math.degrees(math.atan(ratio))
        return angle
    except ZeroDivisionError:
        raise Exception("left shoulder and right shoulder detected at same location.")

def rotate_points(points, source_img, angle):
    # get rotation matrix
    M = cv.getRotationMatrix2D((source_img.shape[1]/2, source_img.shape[0]/2),angle,1)

    # point
    points = np.array(points)
    # add ones
    ones = np.ones(shape=(len(points), 1))
    points_ones = np.hstack([points, ones])

    # transform point
    transformed_points = M.dot(points_ones.T).T
    return transformed_points.astype('int32')


def crop_square(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    mask = np.where(gray_img == 0, 0, 1)
    h, w = mask.shape
    # initialize
    start = [0,0]
    end = [h,w]

    # index
    row, column = np.where(mask==1)

    start[0] = min(row)
    start[1] = min(column)
    end[0] = max(row)
    end[1] = max(column)

    crop = img[start[0]:end[0]+1, start[1]:end[1]+1]
    return start, crop

def blend_images(source, source_shoulder, dest, dest_shoulder):
    "Blend source to dest frame. Start from right shoulder of dest."
    # step 5: crop segmentaton
    start_crop, crop_seg = crop_square(source)

    # calc distance from startcrop to right shoulder
    right_shoulder = source_shoulder[0]
    backoff = [right_shoulder[1]-start_crop[0], right_shoulder[0]-start_crop[1]] # row, col
    print(backoff)

    # blend
    sh, sw = crop_seg.shape[0], crop_seg.shape[1]
    dh = dest.shape[0] - (dest_shoulder[0][1]-backoff[0]) + 10
    dw = dest.shape[1] - (dest_shoulder[0][0]-backoff[1])

    if dh<sh or dw<sw:
        source_square = crop_seg[:dh, :dw, :]
        dest_square = dest[dest.shape[0]-dh:dest.shape[0], dest.shape[1]-dw:dest.shape[1], :]
        gray = cv.cvtColor(source_square,cv.COLOR_BGR2GRAY)
        mask = np.where(cv.cvtColor(gray,cv.COLOR_BGR2GRAY)!=0)
        dest_square[mask] = source_square[mask]
        dest[dest.shape[0]-dh:dest.shape[0], dest.shape[1]-dw:dest.shape[1], :] = dest_square
    else:
        source_square = crop_seg[:, :, :]
        dest_square = dest[dest.shape[0]-dh:dest.shape[0]-dh+sh, dest.shape[1]-dw:dest.shape[1]-dw+sw, :]
        gray = cv.cvtColor(source_square, cv.COLOR_BGR2GRAY)
        mask = np.where(gray!=0)
        print(mask)
        dest_square[mask] = source_square[mask]
        dest[dest.shape[0]-dh:dest.shape[0]-dh+sh, dest.shape[1]-dw:dest.shape[1]-dw+sw, :] = dest_square
    return dest


def fill_holes(img, seg_img):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
    gray_img = cv.cvtColor(seg_img, cv.COLOR_BGR2GRAY)
    closing = cv.morphologyEx(gray_img, cv.MORPH_CLOSE, kernel)
    mask = np.where(closing!=0)
    seg_img[mask] = img[mask]
    return seg_img

def remove_border(img):
    # find outermost cloth contour
    blur_image = cv.GaussianBlur(img, (5,5), 0)
    gray_img = cv.cvtColor(blur_image, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray_img, 1, 255, 0)
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # new mask to draw contours
    mask = np.zeros(img.shape[:2], np.uint8)
    # cv.drawContours(mask, contours, -1, 255, 1)
    cv.fillPoly(mask, pts=contours, color=(255))
    kernel = np.ones((10, 10), np.uint8) # tweak
    mask = cv.erode(mask, kernel, iterations = 1)
    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    print(cnts)

    # find second largest contour
    contour = cnts[0]
    if len(cnts)>1:
        contour = cnts[1]

    # fill target contour with diff color
    cv.fillPoly(mask, pts=[contour], color=200)
    # new img
    new_img = np.zeros(img.shape, dtype='uint8')
    new_img[np.where(mask==200)] = img[np.where(mask==200)]
    return mask, new_img


def get_shoulder_loc(img, is_array=True):
    if is_array:
        frame = img
    else:
        frame = cv.imread(img)

    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    inp = cv.dnn.blobFromImage(frame, inScale, (inWidth, inHeight),
                               (0, 0, 0), swapRB=False, crop=False)
    net.setInput(inp)
    out = net.forward()

    assert(len(BODY_PARTS) <= out.shape[1])

    # find right and left shoulder
    points = []
    for i in [2, 5]:
        # Slice heatmap of corresponding body's part.
        heatMap = out[0, i, :, :]

        _, conf, _, point = cv.minMaxLoc(heatMap)  # (min, max, minloc, maxloc)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]

        # Add a point if it's confidence is higher than threshold.
        points.append((int(x), int(y)) if conf > THRESHOLD else None)

    print("Shoulder Points:",points)
    if points[0] is None or points[1] is None:
        return None

    return points



inWidth = WIDTH
inHeight = HEIGHT
inScale = SCALE

net = cv.dnn.readNet(cv.samples.findFile(protoFile),
                     cv.samples.findFile(weightsFile))


# step 1
# get source image and seg cloth
source_img, source_seg = extract_cloth(SOURCE_IMG)
source_img = cv.cvtColor(source_img, cv.COLOR_RGB2BGR)
source_seg = cv.cvtColor(source_seg, cv.COLOR_RGB2BGR)
print(source_img.shape, source_seg.shape)

# step 1.2: fill holes
source_seg = fill_holes(source_img, source_seg)

# step 2: get source size and rotation angle
source_points = get_shoulder_loc(source_img)
if source_points is None:
    print("Source image w/o shoulder.")
    exit(1) 
source_distance = source_points[1][0] - source_points[0][0]
source_angle = find_rotation_angle(source_points[0], source_points[1])

# step 3: get dest size and rotation angle
dest_frame = cv.imread(DEST_IMG)
dest_points = get_shoulder_loc(dest_frame)
if dest_points is None:
    print("Dest image w/o shoulder.")
    exit(1)
dest_distance = dest_points[1][0] - dest_points[0][0]
dest_angle = find_rotation_angle(dest_points[0], dest_points[1])

print(source_distance)
print(dest_distance)

# step 4: resize source seg and shoulder points
resize_factor = dest_distance/source_distance
print("rf", resize_factor)

source_seg = cv.resize(source_seg,
                         (int(source_seg.shape[1]*resize_factor),
                          int(source_seg.shape[0]*resize_factor))
                         )

source_points[0] = resize_shoulder_coord(source_points[0], resize_factor)
source_points[1] = resize_shoulder_coord(source_points[1], resize_factor)

# step 5: rotate source seg and shoulder points
rotation_angle = dest_angle - source_angle
rotated_seg = imutils.rotate(source_seg, rotation_angle)
source_points = rotate_points(source_points, source_seg, rotation_angle)

print("Rotated:", source_points)

# step 5.2: remove border
mask, clean_seg = remove_border(rotated_seg)

# step 6: blend
final_img = blend_images(clean_seg, source_points, dest_frame, dest_points)


# visualize
source_frame = clean_seg

cv.ellipse(source_frame, tuple(source_points[0]),
           (3, 3), 0, 0, 360, (0, 255, 0), cv.FILLED)
cv.ellipse(source_frame, tuple(source_points[1]),
           (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

source_frame[np.where(mask!=200)] = 255
cv.imshow("ssds", source_frame)

cv.ellipse(dest_frame, dest_points[0], (3, 3),
           0, 0, 360, (0, 255, 0), cv.FILLED)
cv.ellipse(dest_frame, dest_points[1], (3, 3),
           0, 0, 360, (0, 0, 255), cv.FILLED)
cv.imshow("ssdd", dest_frame)

cv.imshow("final", final_img)

cv.waitKey(0)
cv.destroyAllWindows()

