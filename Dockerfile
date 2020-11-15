FROM arm32v5/python:3.9.0-buster AS requirements_builder

RUN pip install pipenv

WORKDIR /tmp
COPY [ "Pipfile", "Pipfile.lock", "/tmp/" ]
ARG PIPENV_IGNORE_VIRTUALENVS=1
RUN pipenv lock --requirements > /tmp/requirements.txt

ARG INKY_VERSION=1.1.1
RUN echo "inky==${INKY_VERSION}" >> /tmp/requirements.txt

ARG RPI_GPIO_VERSION=0.7.0
RUN echo "RPi.GPIO==${RPI_GPIO_VERSION}" >> /tmp/requirements.txt

FROM arm32v5/python:3.9.0-buster

WORKDIR /eink-radiator

COPY --from=requirements_builder /tmp/requirements.txt /eink-radiator/
RUN pip install --requirement /eink-radiator/requirements.txt

COPY *.py               /eink-radiator/
COPY image_sources      /eink-radiator/image_sources
COPY static             /eink-radiator/static
COPY templates          /eink-radiator/templates

VOLUME /data
ENV DATA_FILE_PATH=/data/radiator.pickle
ENV EINK_SCREEN_PRESENT=true
ENV PORT=5000
EXPOSE 5000
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:5000/')"
CMD python radiator.py
