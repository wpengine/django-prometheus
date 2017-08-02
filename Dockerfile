FROM python:3.6

RUN mkdir /app
WORKDIR /app
COPY setup.py requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
