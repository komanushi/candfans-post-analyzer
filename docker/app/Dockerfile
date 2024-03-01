FROM python:3.11.6-bullseye

#RUN apt-get update -y \
#    && apt-get install -y

WORKDIR /app

ADD . /app
RUN pip install poetry==1.8.1

ENTRYPOINT ["/app/docker/app/entrypoint.sh"]
