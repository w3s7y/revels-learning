FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
VOLUME /project
WORKDIR /project
CMD bash
