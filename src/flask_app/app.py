from flask import Flask, flash, render_template, request, redirect, session, url_for
import os
from werkzeug.utils import secure_filename

from controller.image_upload_form import ProfileImageUploadForm, SourceImageUploadForm
from controller.main import download_image

from flask_app import CreateApp
app = create_app()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload_profile_image/', methods=['GET', 'POST'])
def upload_profile_image():
    # check if user has already uploaded
    if 'profile_image' in session.keys():
        if os.path.isfile(os.path.join(app.static_folder, app.config["UPLOAD_FOLDER"], session['profile_image'])):
            return redirect(url_for('upload_source_image'))

    profile_form = ProfileImageUploadForm()
    if request.method=="POST":
        if profile_form.validate_on_submit():
            f = profile_form.profile_image.data
            filename = secure_filename(f.filename)
            # save file
            f.save(os.path.join(app.static_folder, app.config['UPLOAD_FOLDER'], filename))
            session['profile_image'] = filename
            # flash("Success:"+filename, 'success')
            return redirect(url_for('upload_source_image'))
            
    return render_template('upload_profile_image.html', form=profile_form)


@app.route('/upload_source_image/', methods=['GET', 'POST'])
def upload_source_image():
    source_form = SourceImageUploadForm()
    if request.method=="POST":
        if source_form.validate_on_submit():
            image_url = source_form.source_image_url.data
            # download image
            app.logger.info("Downloading Imgae: "+image_url)
            source_image = download_image(image_url, dest_folder=os.path.join(app.static_folder, app.config['UPLOAD_FOLDER']))
            if "404" in source_image:
                source_form.source_image_url.errors.append(source_image)
                return redirect(url_for('upload_source_image'))
            
            session['source_image'] = source_image
            # flash("Success:"+image_url, 'success')
            return redirect(url_for('run_tryon'))
            
    return render_template('upload_source_image.html', form=source_form)


if __name__ == '__main__':
    import logging
    logging.basicConfig(filename=app.root_path+'/logs/cmate.log',level=logging.DEBUG)

    app.run(debug=True)
