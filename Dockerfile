FROM nvidia/cuda:11.5.0-cudnn8-devel-ubuntu20.04

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y python3-pip python3-dev default-libmysqlclient-dev build-essential

ARG PROJECT=machine-text-clf
ARG PROJECT_DIR=/${PROJECT}
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR

COPY . .
RUN pip install -r requirements.txt
RUN pip install torch==1.12.0+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
