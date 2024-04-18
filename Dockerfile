FROM python:3.11-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y libaio1  python3-dev python-dev && apt install nano

WORKDIR /backend
COPY ./requirements.txt /backend/

RUN python -m pip install --upgrade pip

RUN pip install -r /backend/requirements.txt

COPY . /backend/

ENTRYPOINT ["python", "main.py"]
