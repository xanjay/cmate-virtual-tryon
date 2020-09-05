"""
utility functions for image manipulation
"""
import cv2 as cv
import numpy as np


def fill_holes(img, seg_img):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    gray_img = cv.cvtColor(seg_img, cv.COLOR_BGR2GRAY)
    closing = cv.morphologyEx(gray_img, cv.MORPH_CLOSE, kernel)
    mask = np.where(closing != 0)
    seg_img[mask] = img[mask]
    return seg_img


def resize_shoulder_coord(loc, factor):
    return (int(loc[0]*factor), int(loc[1]*factor))


def rotate_shoulder_points(frame, shoulder_points, angle):
    # get rotation matrix
    M = cv.getRotationMatrix2D((frame.shape[1]/2, frame.shape[0]/2), angle, 1)

    # point
    points = np.array(shoulder_points)
    # add ones
    ones = np.ones(shape=(len(points), 1))
    points_ones = np.hstack([points, ones])

    # transform point
    transformed_points = M.dot(points_ones.T).T
    return transformed_points.astype('int32')


def remove_segmentation_border(img, cv2):
    # find outermost cloth contour
    blur_image = cv.GaussianBlur(img, (5, 5), 0)
    gray_img = cv.cvtColor(blur_image, cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray_img, 1, 255, 0)
    contours, _ = cv.findContours(
        thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # new mask to draw contours
    mask = np.zeros(img.shape[:2], np.uint8)
    # cv.drawContours(mask, contours, -1, 255, 1)
    cv.fillPoly(mask, pts=contours, color=(255))
    kernel = np.ones((10, 10), np.uint8)  # tweak
    mask = cv.erode(mask, kernel, iterations=1)
    cnts, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    cnts_area = [cv.contourArea(c) for c in cnts]
    # sort with contour area desc
    cnts = sorted(cnts, key=lambda c:cv.contourArea(c), reverse=True)
    cnts_area = sorted(cnts_area, reverse=True)
    # cv2.imshow("conts", mask)
    # cv2.drawContours(mask, cnts, -1, 127, 5)
    # find second largest contour
    contour = cnts[0]
    # take second largest contour if exists
    if len(cnts) > 1 and cnts_area[0]-cnts_area[1]<1000:
        contour = cnts[1]

    # fill target contour with diff color
    cv.fillPoly(mask, pts=[contour], color=200)
    # new img
    new_img = np.zeros(img.shape, dtype='uint8')
    new_img[np.where(mask == 200)] = img[np.where(mask == 200)]
    return mask, new_img


def crop_square(img):
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    mask = np.where(gray_img == 0, 0, 1)
    h, w = mask.shape
    # initialize
    start = [0, 0]
    end = [h, w]

    # index
    row, column = np.where(mask == 1)

    start[0] = min(row)
    start[1] = min(column)
    end[0] = max(row)
    end[1] = max(column)

    crop = img[start[0]:end[0]+1, start[1]:end[1]+1]
    return start, crop


def blend_images(source_seg, source_shoulder, dest, dest_shoulder):
    "Blend source_seg to dest frame. Start from right shoulder of dest."
    # step 5: crop segmentaton
    start_crop, crop_seg = crop_square(source_seg)

    # calc distance from startcrop to right shoulder
    right_shoulder = source_shoulder[0]
    backoff = [right_shoulder[1]-start_crop[0],
               right_shoulder[0]-start_crop[1]]  # row, col
    # print(backoff)

    # blend
    sh, sw = crop_seg.shape[0], crop_seg.shape[1]
    dh = dest.shape[0] - (dest_shoulder[0][1]-backoff[0]) + 10
    dw = dest.shape[1] - (dest_shoulder[0][0]-backoff[1])

    if dh < sh or dw < sw:
        source_square = crop_seg[:dh, :dw, :]
        dest_square = dest[dest.shape[0]-dh:dest.shape[0],
                           dest.shape[1]-dw:dest.shape[1], :]
        gray = cv.cvtColor(source_square, cv.COLOR_BGR2GRAY)
        mask = np.where(gray != 0)
        dest_square[mask] = source_square[mask]
        dest[dest.shape[0]-dh:dest.shape[0],
             dest.shape[1]-dw:dest.shape[1], :] = dest_square
    else:
        source_square = crop_seg[:, :, :]
        dest_square = dest[dest.shape[0]-dh:dest.shape[0] -
                           dh+sh, dest.shape[1]-dw:dest.shape[1]-dw+sw, :]
        gray = cv.cvtColor(source_square, cv.COLOR_BGR2GRAY)
        mask = np.where(gray != 0)
        # print(mask)
        dest_square[mask] = source_square[mask]
        dest[dest.shape[0]-dh:dest.shape[0]-dh+sh,
             dest.shape[1]-dw:dest.shape[1]-dw+sw, :] = dest_square
    return dest
