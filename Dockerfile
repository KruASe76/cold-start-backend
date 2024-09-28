FROM python:3.12.6-alpine

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD fastapi run main.py --port 8000
