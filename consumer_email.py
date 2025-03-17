import pika
import connect
from model import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='email messages', durable=True)

    def callback_call_phone(ch, method, properties, body):
        id = body.decode()
        Contact.objects(id=id).update(is_message_sent=True)
        print(f"email message is sent - {id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='email messages',
        on_message_callback=callback_call_phone
    )
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting the program...")
        exit(0)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
