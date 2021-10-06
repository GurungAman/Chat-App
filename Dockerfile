FROM python:3.8.5
ENV PYTHONBUFFERED=1
WORKDIR /project
COPY requirements-dev.txt /project/
RUN pip install -r requirements-dev.txt
COPY . /project/