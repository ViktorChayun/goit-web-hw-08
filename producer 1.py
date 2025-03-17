import pika
import connect
from model import Contact
from faker import Faker


SIZE = 100
faker = Faker("uk-UA")


def generate_contacts(size: int, channel):
    for _ in range(size):
        c = Contact(full_name=faker.full_name(), email=faker.email())
        c.save()
        channel.basic_publish(
            exchange='',
            routing_key='contact messages',
            body=str(c.id).encode()
        )


if __name__ == "__main__":
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='contact messages')

    generate_contacts(SIZE, channel)
    connection.close()
