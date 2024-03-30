"""
This is a worker that listens to the 'upload' queue and prints the message it receives.
Messages are processed with output stored in the database.
"""

import sys
import os
import logging
import pika
from pika.adapters.blocking_connection import BlockingChannel
from .config import Config


logger = logging.getLogger(__name__)


def conect(
        host: str = "rabbitmq",
        quque_name: str = "upload",
        connection_attempts: int = 3,
        connection_delay: int = 10) -> BlockingChannel:
    """
    Connect to RabbitMQ and return a channel

    When starting if the RabbitMQ is not ready, the worker will try to connect to it every 10
    seconds 3 times.

    :param host: str: RabbitMQ host
    :param quque_name: str: Queue name
    :param connection_attempts: int: Number of connection attempts
    :param connection_delay: int: Delay between connection attempts
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host,
                                  connection_attempts=connection_attempts,
                                  retry_delay=connection_delay))
    channel = connection.channel()

    channel.queue_declare(queue=quque_name)

    return channel


def main():
    c = Config()
    log_level = c.get('logs', 'log_level')
    logging.basicConfig(level=log_level)
    channel = conect(
        host=c.get('rabbitmq', 'host'),
        quque_name=c.get('rabbitmq', 'queue')
    )

    def callback(ch, method, properties, body):
        logging.info("Received %s", body)
        logging.debug("Method: %s", method)
        logging.debug("Properties: %s", properties)
        logging.debug("Channel: %s", ch)

    channel.basic_consume(
        queue='upload', on_message_callback=callback, auto_ack=True)

    logger.info('Waiting for messages. To exit press CTRL+C')
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
