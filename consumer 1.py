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
    channel.queue_declare(queue='contact messages')

    def callback_send_email(ch, method, properties, body):
        id = body.decode()
        Contact.objects(id=id).update(is_message_sent=True)
        print(f"Send email {id}")

    channel.basic_consume(
        queue='contact messages',
        on_message_callback=callback_send_email,
        auto_ack=True
    )
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
