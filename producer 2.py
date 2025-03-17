import pika
import connect
from model import Contact
from faker import Faker


SIZE = 100
faker = Faker("uk-UA")


def generate_contacts(size: int, channel):
    for _ in range(size):
        c = Contact(
            full_name=faker.full_name(),
            email=faker.email(),
            phone=faker.phone_number(),
            preferred_channel=faker.random_element(elements=("email", "sms"))
        )
        c.save()
        channel.basic_publish(
            exchange='Contacts',
            routing_key=c.preferred_channel,
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

    channel.exchange_declare(exchange='Contacts', exchange_type='direct')
    channel.queue_declare(queue='email messages', durable=True)
    channel.queue_declare(queue='sms messages', durable=True)

    channel.queue_bind(exchange='Contacts', queue='email messages', routing_key='email')
    channel.queue_bind(exchange='Contacts', queue='sms messages', routing_key='sms')

    generate_contacts(SIZE, channel)
    connection.close()
