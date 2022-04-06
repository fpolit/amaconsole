FROM ubuntu:20.04

RUN apt -y update && apt -y full-upgrade
RUN apt -y install gcc g++ python3.8 python3.8-dev make cmake libboost-python-dev # required dependencies
RUN apt -y install python3-setuptools sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker