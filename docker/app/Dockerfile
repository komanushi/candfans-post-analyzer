FROM python:3.11.6-bullseye

RUN apt-get update -y \
    && apt-get install -y

WORKDIR /app
ADD ./pyproject.toml /app
ADD ./poetry.lock /app


RUN pip install poetry==1.8.1

RUN poetry install && \
    rm -rf /root/.cache/pypoetry/artifacts

ADD . /app
ADD ./docker/app/.bashrc /root/.bashrc

ENTRYPOINT ["/app/docker/app/entrypoint.sh"]
