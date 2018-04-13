FROM ubuntu
RUN apt-get update && apt-get install -y python3 python3-pip
ADD . /project
RUN pip3 install -r /project/requirements.txt
WORKDIR /project
CMD bash
