FROM ubuntu:latest
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install python3-dev -y
RUN apt-get install libmysqlclient-dev -y
ADD . /datalogger
WORKDIR /datalogger
RUN pip3 install -r requirements.txt
CMD python3 app.py
