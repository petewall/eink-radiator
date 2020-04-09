FROM arm32v5/python:3.7-buster AS requirements_builder

RUN pip install pipenv

WORKDIR /tmp
COPY [ "Pipfile", "Pipfile.lock", "/tmp/" ]
ARG PIPENV_IGNORE_VIRTUALENVS=1
RUN pipenv lock --requirements > /tmp/requirements.txt

ARG INKY_VERSION=0.0.5
RUN echo "inky==${INKY_VERSION}" >> /tmp/requirements.txt

FROM arm32v5/python:3.7-buster

WORKDIR /eink-radiator

COPY --from=requirements_builder /tmp/requirements.txt /eink-radiator/
RUN pip install --requirement /eink-radiator/requirements.txt

COPY \
    controller.py \
    radiator.py \
    screen.py \
    \
    /eink-radiator/
COPY image_sources /eink-radiator/image_sources
COPY static /eink-radiator/static
COPY templates /eink-radiator/templates

ENV EINK_SCREEN_PRESENT=true
CMD python controller.py
