FROM python:3.12

MAINTAINER "whywaita <https://github.com/whywaita>"

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y opencv-data libgl1-mesa-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml /app/pyproject.toml
RUN poetry install

COPY . /app
CMD poetry run python3 main.py launch-webserver