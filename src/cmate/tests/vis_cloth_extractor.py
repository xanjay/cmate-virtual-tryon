"visualize cloth extractor"

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from cmate_main import CMate

from segmentation.cloth_extractor import run_visualization

# test run
SAMPLES_DIR = os.environ['ROOT_DIR']+"/src/flask_app/static/images/samples"
SOURCE_IMG = SAMPLES_DIR+"/source_images/sample-source-image1.jpg"

run_visualization(SOURCE_IMG)