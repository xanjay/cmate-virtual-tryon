# from app.controller.main import download_image
from .app import app
from flask_app.controller.utils import download_image
import os


def test_image_download():
    image_url = ""
    dest_dir = os.path.join(app.config['static_url_path'],
                     app.config['UPLOAD_FOLDER'])
    filename = download_image(image_url, dest_dir)

    assert os.path.isfile(
        os.path.join(app.config['static_url_path'],
                     app.config['UPLOAD_FOLDER'], filename)) is True

print(app)