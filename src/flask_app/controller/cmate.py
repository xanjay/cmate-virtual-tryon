from datetime import datetime
from pathlib import Path
import cv2
import sys

# add cmate to PYTHONPATH
sys.path.insert(1, str(Path(__file__).resolve().parent.parent.parent/'cmate'))
from cmate_main import CMate

def blend_images(profile_img, source_img, profile_dir, source_dir, dest_dir):
    "apply cloth to profile image and save to result"
    # verify file exists
    if not (Path(profile_dir)/profile_img).exists():
        raise FileNotFoundError("Profile Image not found.")
    if not (Path(source_dir)/source_img).exists():
        raise FileNotFoundError("Source Image not found.")
    # apply cmate
    cloth_blender = CMate(str(Path(source_dir)/source_img),
                          str(Path(profile_dir)/profile_img))
    final_img, errors = cloth_blender.apply_cloth()
    filename = "result-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg"
    cv2.imwrite(str(Path(dest_dir)/filename), final_img)
    return filename, errors
