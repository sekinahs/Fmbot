FROM python:3.8-slim-buster
WORKDIR /app

COPY . .

RUN pip3 install -U -r requirements.txt

CMD bash start.sh
