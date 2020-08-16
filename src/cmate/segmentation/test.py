import imutils
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


img = cv.imread("C:\\Users\\sanja\\Desktop\\test_rotatedseg.jpg")


# original
# cv.imshow("img", img)

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



mask, clean_img = remove_border(img)
clean_img[np.where(mask!=200)] = 255
cv.imshow("ffll", clean_img)


img[np.where(img==0)] = 255
cv.imshow("img", img)

cv.waitKey(0)
cv.destroyAllWindows()

exit(0)

# contour
"""
blur_image = cv.GaussianBlur(img, (5,5), 0)
gray_img = cv.cvtColor(blur_image, cv.COLOR_BGR2GRAY)

_, thresh = cv.threshold(gray_img, 1, 255, 0)
contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

large_contour = contours[0]
for c in contours:
    if cv.contourArea(large_contour) < cv.contourArea(c):
        large_contour = c
cv.fillPoly(img, pts=[large_contour], color=(0,255,0))
"""

th, im_th = cv.threshold(img, 1, 255, 0)
# Copy the thresholded image.
im_floodfill = im_th.copy()

 
# Mask used to flood filling.

# Notice the size needs to be 2 pixels than the image.

h, w = im_th.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Floodfill from point (0, 0)

cv.floodFill(im_floodfill, mask, (0,0), 255)


# final
cv.imshow("img", img)
cv.imshow("ffll", im_floodfill)

cv.waitKey(0)
cv.destroyAllWindows()


# cnts = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# cv2.drawContours(image, cnts, -1, 0, 15) 
# 15 is the right thickness for this image, but might not be for other ones...