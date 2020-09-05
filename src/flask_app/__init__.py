from flask import Flask
from pathlib import Path
import sys

import logging
from datetime import datetime

from config import app_config

def create_app():

    # Set the secret key to some random bytes. Keep this really secret!
    config = {
        "DEBUG": True,
        "SECRET_KEY": b"xanjay_secrect",
        "CACHE_TYPE": "simple",  # Flask-Caching related configs
        "CACHE_DEFAULT_TIMEOUT": 300
    }
    # initiate flask instance
    app = Flask(__name__)

    # tell Flask to use the above defined config
    app.config.from_mapping(config)

    # setup logging
    app = setup_logging(app)
    
    return app

def setup_logging(app):
    log_file = "cmate-"+datetime.now().strftime('%Y-%m-%d')+".log"
    logging.basicConfig(filename=app.root_path + '/logs/'+ log_file, level=logging.DEBUG)
    return app

