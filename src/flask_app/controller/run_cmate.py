from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import os

from controller.main import download_image, blend_images

bp = Blueprint('tryon', __name__, url_prefix='/tryon')

@bp.route('/tryon/', methods=['GET', 'POST'])
def run_tryon():
    profile_image = session['profile_image']
    source_image = session['source_image']
    result_image = blend_images(profile_image, source_image, images_dir=os.path.join(
        bp.static_folder, bp.config['UPLOAD_FOLDER']))
    print("profile:", profile_image)
    print("source:", source_image)
    print("result:", result_image)
    flash("Oops!!", 'danger')

    return render_template('tryon_result_page.html',
                           profile_image=bp.config['UPLOAD_FOLDER'] +
                           '/'+profile_image,
                           source_image=bp.config['UPLOAD_FOLDER'] +
                           '/'+source_image,
                           result_image=bp.config['UPLOAD_FOLDER']+'/'+result_image)
