from flask import (flash, render_template, request, redirect,
                   session, url_for, send_from_directory)

from pathlib import Path
from werkzeug.utils import secure_filename
from collections import defaultdict

from controller.image_upload_form import ProfileImageUploadForm, SourceImageUploadForm
from controller.utils import session_alive, download_image
from controller.cmate import blend_images
from config import app_config

from __init__ import create_app
app = create_app()

cache = defaultdict(str)


@app.route('/')
def home():
    profile_image = None
    if session_alive():
        profile_image = session['profile_image']
    return render_template('index.html', profile_image=profile_image)

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/upload_profile_image/', methods=['GET', 'POST'])
def upload_profile_image():
    # check if user has already uploaded profile picture and no need to update
    if session_alive() and len(request.args.getlist('updateprofile')) != True:
        return redirect(url_for('upload_source_image'))

    profile_form = ProfileImageUploadForm()
    if request.method == "POST":
        if profile_form.validate_on_submit():
            f = profile_form.profile_image.data
            filename = secure_filename(f.filename)
            # save file
            f.save(str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']/filename))
            session['profile_image'] = filename
            # flash("Success:"+filename, 'success')
            # redirect to desired endpoint
            if len(request.args.getlist('nextpage')) > 0:
                return redirect(url_for(request.args.get('nextpage')))

            return redirect(url_for('upload_source_image'))

    profile_image = None
    if session_alive():
        profile_image = session['profile_image']
    return render_template('upload_profile_image.html',
                           form=profile_form, profile_image=profile_image)


@app.route('/upload_source_image/', methods=['GET', 'POST'])
def upload_source_image():
    source_form = SourceImageUploadForm()
    if request.method == "POST":
        if source_form.validate_on_submit():
            image_url = source_form.source_image_url.data
            # download image
            app.logger.info("Downloading Imgae: "+image_url)
            source_image = download_image(image_url, 
                           dest_folder=str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']))
            if "404" in source_image:
                flash(source_image, 'danger')
                return redirect(url_for('upload_source_image'))

            session['source_image'] = source_image
            # flash("Success:"+image_url, 'success')
            return redirect(url_for('tryon'))

    profile_image = None
    if session_alive():
        profile_image = session['profile_image']
    return render_template('upload_source_image.html',
                           form=source_form, profile_image=profile_image)


@app.route('/tryon/', methods=['GET', 'POST'])
def tryon():
    try:
        profile_image = session['profile_image']
        source_image = session['source_image']
        # check cache
        if cache['profile_image'] == profile_image and cache['source_image'] == source_image:
            result_image, warnings = cache['result_image'],cache['warnings']
        else:
            result_image, warnings = blend_images(profile_image, source_image,
                                    images_dir=str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']),
                                    dest_dir=str(Path(app_config["FILES_DIR"])/app_config['RESULT_FOLDER']))
            # set cache
            cache['profile_image'] = profile_image
            cache['source_image'] = source_image
            cache['result_image'] = result_image
            cache['warnings'] = warnings

        if len(warnings) > 0:
            for e in warnings:
                flash(e, 'warning')
        
        # flash("Successful try on!", 'success')
    except Exception as e:
        flash(str(e)+"\nTry new image.", 'danger')
        result_image = ""
        # set cache
        cache['profile_image'] = profile_image
        cache['source_image'] = source_image
        cache["warnings"] = [str(e)]

    return render_template('tryon_result_page.html',
                           profile_image=profile_image,
                           source_image=source_image,
                           result_image=result_image)


@app.route('/download/<path:filename>')
def download_file(filename):
    flash("Successfully downloaded !", 'success')
    return send_from_directory(str(Path(app_config["FILES_DIR"])/app_config['RESULT_FOLDER']),
                               secure_filename(filename), as_attachment=True)


@app.route('/uploaded_images/<path:filename>')
def get_uploaded_image(filename):
    return send_from_directory(str(Path(app_config["FILES_DIR"])/app_config['UPLOAD_FOLDER']),
                               secure_filename(filename))


@app.route('/result_images/<path:filename>')
def get_result_image(filename):
    return send_from_directory(str(Path(app_config["FILES_DIR"])/app_config['RESULT_FOLDER']),
                               secure_filename(filename))


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename=app.root_path +
                        '/logs/cmate.log', level=logging.INFO)

    app.run()
