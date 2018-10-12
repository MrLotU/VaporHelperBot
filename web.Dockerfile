FROM python:2.7.13

ENV ENV docker

RUN mkdir /opt/VaporHelper
ADD requirements.txt /opt/VaporHelper
ADD . /opt/VaporHelper/

WORKDIR /opt/VaporHelper

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "bot", "-e", "docker"]