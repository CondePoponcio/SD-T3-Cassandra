FROM python:3.8.10

RUN apt update

RUN apt install -y lsof

WORKDIR /workspace

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

