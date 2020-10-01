FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3.6 \
    python3-pip python3-venv sudo
RUN apt-get install build-essential python-dev -y

# INSTALL TKINTER FOR Matplotlib-Ubuntu
# ARG DEBIAN_FRONTEND=noninteractive
# ENV TZ=Europe/Moscow
# RUN apt-get install python3-tk -y

# create cmate user and add to sudoers
# RUN useradd -m cmate
# RUN usermod -aG sudo cmate
# RUN echo '%cmate ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir -p /opt/cmate/
COPY . /opt/cmate/

# set root dir
ENV ROOT_DIR="/opt/cmate"

#create venv
# RUN pip3 install virtualenv
RUN python3.6 -m venv ./venv
RUN /bin/bash -c "source ./venv/bin/activate"

# upgrade pip3
RUN pip3 install --upgrade pip

RUN cd /opt/cmate/ && pip3 install -r requirements.txt
WORKDIR /opt/cmate/src/flask_app/

EXPOSE 8080
# ENTRYPOINT uwsgi --ini cmate.ini
