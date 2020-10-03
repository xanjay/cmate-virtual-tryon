from flask import Flask
import os
from pathlib import Path
import sys

import logging
from datetime import datetime

from .config import app_config
from .controller.utils import (create_dirs, prepare_sample_images)

PROFILE_DIR = str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']/'profile_images')
SOURCE_DIR = str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']/'source_images')
RESULT_DIR = str(Path(app_config["FILES_DIR"])/app_config['RESULT_FOLDER'])

def create_app():

    # Set the secret key to some random bytes. Keep this really secret!
    config = {
        "DEBUG": True,
        "SECRET_KEY": app_config["SECRET_KEY"],
        "CACHE_TYPE": "simple",  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": 300,
        "PROFILE_DIR": PROFILE_DIR,
        "SOURCE_DIR": SOURCE_DIR,
        "RESULT_DIR": RESULT_DIR
    }
    # initiate flask instance
    app = Flask(__name__)

    # tell Flask to use the above defined config
    app.config.from_mapping(config)

    # setup logging
    app = setup_logging(app)

    # Initialize dirs and sample files
    create_dirs([PROFILE_DIR,SOURCE_DIR,RESULT_DIR])
    prepare_sample_images()
    
    return app

def setup_logging(app):
    if not os.path.exists(app_config["LOGS_DIR"]):
        os.makedirs(app_config["LOGS_DIR"])

    log_file = "cmate-"+datetime.now().strftime('%Y-%m-%d')+".log"
    logging.basicConfig(filename=app.root_path + '/logs/'+ log_file, level=logging.ERROR)
    return app

