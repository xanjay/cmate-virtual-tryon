from flask import session
from datetime import datetime
import urllib.request
import sys
from pathlib import Path

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


def session_alive():
    " check if user has already uploaded profile image"
    if 'profile_image' in session.keys():
        if (Path(app_config["FILES_DIR"])/app_config["UPLOAD_FOLDER"]/session['profile_image']).is_file():
            return True
    return False