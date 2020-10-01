import os

app_config = {
    "INSTANCE_PATH": os.path.join(os.environ["ROOT_DIR"], "src", "flask_app"),
    "FILES_DIR": os.path.join(os.environ["ROOT_DIR"], "src", "flask_app", "files"),
    "UPLOAD_FOLDER": "user_uploads",
    "RESULT_FOLDER": "result_images",
    "LOGS_DIR": os.path.join(os.environ["ROOT_DIR"], "src", "flask_app", "logs"),
    "SECRET_KEY": os.environ.get('SECRET_KEY')
}