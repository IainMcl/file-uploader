"""
This is a worker that listens to the 'upload' queue and prints the message it receives.
Messages are processed with output stored in the database.
"""

import sys
import os
import logging
import pika
from pika.adapters.blocking_connection import BlockingChannel


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def conect(host: str = "rabbitmq", quque_name: str = "upload") -> BlockingChannel:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, connection_attempts=3, retry_delay=10))
    channel = connection.channel()

    channel.queue_declare(queue=quque_name)

    return channel


def main():
    channel = conect()

    def callback(ch, method, properties, body):
        logging.info(f" [x] Received {body}")

    channel.basic_consume(
        queue='upload', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
