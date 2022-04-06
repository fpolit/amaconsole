FROM ubuntu:20.04

RUN apt -y update && apt -y full-upgrade
RUN apt -y install gcc g++ python3.8 python3.8-dev libboost-python-dev # required dependencies
RUN apt -y install python3-setuptools make cmake sudo # build dependencies

RUN useradd -m -u 970 jenkins && echo "jenkins:jenkins" | chpasswd
RUN echo -e "\njenkins\tALL=(root) NOPASSWD: $(which make)" >> /etc/sudoers
RUN cat -n /etc/sudoers
RUN visudo --check
RUN cat /etc/passwd /etc/shadow
USER jenkins