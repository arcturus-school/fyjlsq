FROM python:3.11.1-slim

RUN mkdir -p /usr/src/server

WORKDIR /usr/src/server

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]