FROM ubuntu:20.04
RUN apt -y update && apt -y full-upgrade
# install dependencies
RUN apt -y install gcc g++ python3.8 python3.8-dev make cmake libboost-python-dev
#RUN apt -y install libboost-all-dev