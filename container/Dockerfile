FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python blender
RUN apt install -y python3-pip
RUN pip3 install nibabel dipy 

RUN apt install -y xvfb x11-xkb-utils
RUN pip3 install xvfbwrapper
