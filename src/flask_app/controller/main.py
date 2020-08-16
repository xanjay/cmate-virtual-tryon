from datetime import datetime
import os
import sys
import urllib.request
import cv2

# add flask_app to PYTHONPATH
#TODO: change cmake main dir
sys.path.insert(0, 'E:\\Sanjay\\mlprojects\\virtual_try_on\\src\\cmate')
from cmate_main import CMate

# add flask_app to PYTHONPATH
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from app import app

def download_image(image_url, dest_folder):
    "download image and save to user uploads"
    try:
        filename = "image-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg"
        filepath = os.path.join(dest_folder, filename)
        urllib.request.urlretrieve(image_url, filepath)
        return filename
    except urllib.error.HTTPError:
        return "404:Invalid Image URL"

    
    

def blend_images(profile_img, source_img, images_dir):
    "apply cloth to profile image and save to result"
    cloth_blender = CMate(os.path.join(images_dir, source_img), os.path.join(images_dir, profile_img))
    final_img = cloth_blender.apply_cloth()
    filename = "result-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg"
    cv2.imwrite(os.path.join(images_dir, filename), final_img)
    return filename
