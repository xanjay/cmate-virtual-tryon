from flask import session
from datetime import datetime
import os
from pathlib import Path
import sys
import shutil
import urllib.request

# flask_app/config
sys.path.insert(1, str(Path(__file__).resolve().parent.parent))
from config import app_config

def download_image(image_url, dest_folder):
    "download image and save to user uploads"
    try:
        filename = "image-"+datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+".jpg"
        filepath = Path(dest_folder)/filename
        urllib.request.urlretrieve(image_url, filepath)
        return filename
    except urllib.error.HTTPError:
        return "404:Invalid Image URL"
    except Exception as e:
        return "Error during Image download:\n" + str(e)


def session_alive(profile_dir):
    " check if user has already uploaded profile image"
    if 'profile_image' in session.keys():
        if (Path(profile_dir)/session['profile_image']).is_file():
            return True
    return False

def create_dirs(dirs):
    "create dirs if not exists"
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

def prepare_sample_images():
    # copy sample images to files dir
    files_dir = os.path.join(app_config["FILES_DIR"], app_config['UPLOAD_FOLDER'])

    samples_dir = os.path.join(app_config["INSTANCE_PATH"], "static", "images", "samples")
    profile_dir = os.path.join(samples_dir, "profile_images")
    source_dir = os.path.join(samples_dir, "source_images")
    # copy profile images
    for img in os.listdir(profile_dir):
        shutil.copyfile(os.path.join(profile_dir, img), os.path.join(files_dir, "profile_images", img))
    # copy source images
    for img in os.listdir(source_dir):
        shutil.copyfile(os.path.join(source_dir, img), os.path.join(files_dir, "source_images", img))
