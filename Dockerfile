FROM arm32v5/python:3.9.0-buster AS requirements_builder

RUN pip install pipenv

WORKDIR /tmp
COPY [ "Pipfile", "Pipfile.lock", "/tmp/" ]
ARG PIPENV_IGNORE_VIRTUALENVS=1
RUN pipenv lock --requirements > /tmp/requirements.txt

ARG INKY_VERSION=1.1.1
ARG RPI_GPIO_VERSION=0.7.0

RUN echo "inky==${INKY_VERSION}" >> /tmp/requirements.txt
RUN echo "RPi.GPIO==${RPI_GPIO_VERSION}" >> /tmp/requirements.txt
RUN echo "--extra-index-url https://www.piwheels.org/simple" >> /tmp/requirements.txt
RUN echo "--prefer-binary" >> /tmp/requirements.txt

RUN cat /tmp/requirements.txt

# Greatly speed up package install time by using pre-built packages for Raspberry Pi:
RUN echo "--extra-index-url https://www.piwheels.org/simple" >> /tmp/requirements.txt
RUN echo "--prefer-binary" >> /tmp/requirements.txt

# except for numpy. Using the wheel is causing this error: ModuleNotFoundError: No module named 'numpy.core._multiarray_umath'
RUN echo "--no-binary numpy # Using binaries " >> /tmp/requirements.txt
# ... and Pillow. Using the wheel is causing this error: ImportError: cannot import name '_imaging' from 'PIL'
RUN echo "--no-binary Pillow # Using binaries " >> /tmp/requirements.txt

RUN cat /tmp/requirements.txt

FROM arm32v5/python:3.9.0-buster

WORKDIR /eink-radiator

COPY --from=requirements_builder /tmp/requirements.txt /eink-radiator/
RUN pip install --upgrade pip && \
    pip install --requirement /eink-radiator/requirements.txt

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
