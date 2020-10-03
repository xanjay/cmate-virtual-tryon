# CMate - Installation

## Dependencies
- Python3.6 or above
- Tensorflow 1.15.0
- Opencv 4.2
### Operating System
- Ubuntu 18.04 or above<br>
Note: CMate can be run on Windows with slight modifications on file path format.

### GPU Support
By default, CMate uses Tensorflow CPU. If you have high performance GPU, you can pip install `tensorflow-gpu 1.15.0` to further improve performance.

You can quickly install CMate using docker image:
```
~ sudo docker pull xanjay/cmate
~ sudo docker run -p 8080:8080 -t cmate .
```
Access web app:`http://0.0.0.0:8080`
If you choose to install from source, please follow below steps:

## Step 1: Download OR Clone this repository
 ```
 git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
 ```
## Step 2: Set Environment Variables
```
~ export ROOT_DIR="/path/to/cmate"
~ export SECRET_KEY="some_secret_text" # generate using os.urandom(20)
```
## Step 3: Install Dependencies
First setup python3 virtual environment and install dependencies using requirements file.
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
Note: set `--eager-loading` in flask run command if you need to run flask in debug mode.
```
~ cd $ROOT_DIR/src/flask_app/
~ export FLASK_APP=wsgi.py
~ flask run --host=0.0.0.0 --port=8080
```

## Access CMate Web App
```
http://0.0.0.0:8080
```

