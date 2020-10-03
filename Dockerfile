FROM python:3.6-slim-buster

RUN apt-get update && apt-get install -y python3.6 \
    python3-pip python3-venv sudo
RUN apt-get install build-essential python-dev -y

# INSTALL TKINTER FOR Matplotlib-Ubuntu
# ARG DEBIAN_FRONTEND=noninteractive
# ENV TZ=Europe/Moscow
# RUN apt-get install python3-tk -y

RUN mkdir -p /opt/cmate/
COPY . /opt/cmate/

# set env variables
ENV ROOT_DIR="/opt/cmate"
ENV SECRET_KEY="your_own_secret_key"
ENV FLASK_APP=wsgi.py
# For flask run command
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

#create venv
RUN python3.6 -m venv ./venv
RUN /bin/bash -c "source ./venv/bin/activate"

# upgrade pip3
RUN pip3 install --upgrade pip

RUN cd /opt/cmate/ && pip3 install --no-cache-dir -r requirements.txt --default-timeout=1000
WORKDIR /opt/cmate/src/flask_app/

EXPOSE 8080
ENTRYPOINT flask run --host=0.0.0.0 --port=8080
