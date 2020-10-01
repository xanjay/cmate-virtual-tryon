import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from controller.utils import download_image

from config import app_config

def test_image_download():
    image_url = ""
    dest_dir = os.path.join(app_config["FILES_DIR"],app_config['UPLOAD_FOLDER'],'source_images')

    filename = download_image(image_url, dest_dir)

    assert os.path.isfile(os.path.join(dest_dir, filename)) is True

# print(app)