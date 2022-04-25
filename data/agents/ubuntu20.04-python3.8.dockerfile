FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt -y full-upgrade
RUN apt -y install gcc g++ python3.8 python3.8-dev # required dependencies
RUN apt -y install python3-setuptools python3-pip git make cmake sudo # build dependencies

# AMAPROTO - dependencies
RUN apt -y install libprotoc-dev protobuf-compiler
RUN python3 -m pip install grpcio grpcio-tools

# AMACORE - dependecies
RUN apt -y install libboost-python-dev libboost-program-options-dev

## AMACORE PLUGIN - stegseek
RUN apt -y install libmhash-dev libmcrypt-dev libjpeg8-dev zlib1g-dev


RUN useradd -m -u 970 jenkins && echo "jenkins:jenkins" | chpasswd
RUN echo "jenkins ALL=(root) NOPASSWD: $(which make)" >> /etc/sudoers
RUN visudo --check

USER jenkins
