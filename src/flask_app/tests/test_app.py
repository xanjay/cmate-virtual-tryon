# from app.controller.main import download_image
from .app import app
import os


def test_image_download():
    image_url = ""
    filename = download_image(image_url)

    assert os.path.isfile(
        os.path.join(app.config['static_url_path'],
                     app.config['UPLOAD_FOLDER'], filename)) is True

print(app)