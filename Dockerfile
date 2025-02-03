FROM python:3.11


RUN mkdir "app"
COPY . "app"
WORKDIR "app"

RUN apt-get update && pip install -r requirements.txt
#RUN python manage.py collectstatic --clear
#RUN python manage.py migrate
#RUN python manage.py seed

EXPOSE 8000
