import pika
import json
import time
import requests

RABBIT_URL = "amqp://guest:guest@rabbit:5672/"
QUEUE = "observer.60.q"

API_URL = "http://master:8000/packages"

def connect_with_retry(params):
    while True:
        try:
            print("⏳ Intentando conectar a Rabbit...")
            connection = pika.BlockingConnection(params)
            print("🟢 Conectado a Rabbit!")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("❌ Rabbit no disponible, reintentando en 5s...")
            time.sleep(5)

def callback(ch, method, properties, body):
    data = json.loads(body)

    print("📩 Enviando a API...")

    response = requests.post(API_URL, json=data)

    print("✅ Status:", response.status_code)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    params = pika.URLParameters(RABBIT_URL)


    connection = connect_with_retry(params)
    channel = connection.channel()

    print("🟢 Conectado!")
    channel.basic_consume(
        queue=QUEUE,
        on_message_callback=callback
    )
    channel.start_consuming()

if __name__ == "__main__":
    main()

