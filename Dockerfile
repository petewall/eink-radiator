FROM arm32v5/python:3.8-buster

WORKDIR /
COPY ["requirements.txt", "/"]
RUN pip install --requirement /requirements.txt

COPY ["concourse.py", "/"]
CMD ["python" "/concourse.py"]
