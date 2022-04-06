FROM ubuntu:20.04

RUN apt -y update && apt -y full-upgrade
RUN apt -y install gcc g++ python3.8 python3.8-dev make cmake libboost-python-dev # required dependencies
RUN apt -y install python3-setuptools sudo

RUN useradd -m docker && echo "docker:docker" | chpasswd
RUN echo 'docker ALL=(root) NOPASSWD:make' >> /etc/sudoers # allow run: sudo make -C build/ install
USER docker