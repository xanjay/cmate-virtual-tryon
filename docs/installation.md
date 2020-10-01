# CMate - Installation

## Dependencies
- Tensorflow 1.15.0
- Opencv 4.2
### Operating System
- Ubuntu 18.04 or greater<br>
Note: CMate can be run on Windows with slight modifications on file path format.

### GPU Support
By default, CMate uses Tensorflow CPU. If you have high performance GPU, you can pip install `tensorflow-gpu 1.15.0` to further improve performance.

You can quickly install CMate using docker image. If you choose to install from source, please follow below steps:

## Step 1: Download OR Clone this repository
 ```
 git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
 ```
## Step 2: Set Environment Variable
```
~ export ROOT_DIR="/path/to/cmate"
~ export SECRET_KEY="some_secrect_text" # generate using os.urandom(20)
```
## Step 3: Install Dependencies
First setup python3 virtual environment and install dependencies using requirements file.
### Dependencies
```
~ cd $ROOT_DIR
~ pip install -r requirements.txt
```
### Matplotplib support for ubuntu (Optional)
Install Python tkinter if you want to try on test visualization scripts.
```
sudo apt-get install python3-tk -y
```

## Step 4: Run Flask App
Either run uWSGI server or simply run `app.py`.
```
~ cd $ROOT_DIR/src/flask_app/
~ uwsgi --ini cmate.ini
```

