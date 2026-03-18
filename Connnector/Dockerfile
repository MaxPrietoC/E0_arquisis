FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install pika requests

CMD ["python", "connector.py"]