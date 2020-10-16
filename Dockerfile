FROM debian:latest

RUN apt-get update && apt-get install -y python3-pip git nginx
RUN pip3 install --upgrade pip

COPY requirements.txt /usr/src/ikaria/requirements.txt
RUN pip3 install -r /usr/src/ikaria/requirements.txt

COPY xb1/ /usr/src/ikaria/xb1/
WORKDIR /usr/src/ikaria/xb1/

CMD ["python3", "manage.py runserver"]