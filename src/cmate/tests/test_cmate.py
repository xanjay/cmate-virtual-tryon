import cv2 as cv
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cmate_main import CMate

# test run
SOURCE_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\vest.jpg"
DEST_IMG = "C:\\Users\\sanja\\Desktop\\pose_test\\figure-above.jpg"

def visualize_cmate():
    cloth_blender = CMate(SOURCE_IMG, DEST_IMG)
    final_img, _ = cloth_blender.apply_cloth()
    
    plt.figure(figsize=(12,4))
    
    plt.subplot(1,3,1)
    source_frame = plt.imread(SOURCE_IMG)
    plt.imshow(source_frame)
    plt.title("Source Image")

    plt.subplot(1,3,2)
    dest_frame = plt.imread(DEST_IMG)
    plt.imshow(dest_frame)
    plt.title("Source Image")

    plt.subplot(1,3,3)
    plt.imshow(cv.cvtColor(final_img, cv.COLOR_BGR2RGB))
    plt.title("Final Image")
    
    # plt.imshow(final_img)

    plt.axis("off")
    plt.show()

visualize_cmate()