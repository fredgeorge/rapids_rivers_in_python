# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
#

import pika

from rapidsrivers.rapids.validae_service import validate_service
from rapidsrivers.rivers.river import River


class RabbitMqRapidsConnection:
    DEFAULT_MAXIMUM_READ_COUNT = 9
    EXCHANGE_NAME = 'rapids'
    RABBIT_MQ_PUB_SUB = 'fanout'

    def __init__(self, host, port):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, port=int(port)))
        self._channel = connection.channel()
        self._channel.exchange_declare(
            exchange=self.EXCHANGE_NAME,
            exchange_type=self.RABBIT_MQ_PUB_SUB,
            durable=True,
            auto_delete=True
        )
        self._river = None

    def register(self, service):
        validate_service(service)
        self._river = River(self, service.rules, self.DEFAULT_MAXIMUM_READ_COUNT)  # No sharing of Rivers in this implementation
        queue_name = service.name  # queue name can be same as service name in this implementation
        self._river.register(service)
        self._configure_queue_as_river(queue_name)
        print(' [*] [service: {0}] Waiting for messages. To exit press CTRL+C'.format(service.name))
        self._consume_messages(queue_name)

    def publish(self, message_or_packet):
        is_packet = hasattr(message_or_packet, 'to_json_string')
        message = message_or_packet if not is_packet else message_or_packet.to_json_string()
        self._channel.basic_publish(
            exchange=self.EXCHANGE_NAME,
            routing_key='',
            body=message
        )

    def _configure_queue_as_river(self, queue_name):
        self._channel.queue_declare(queue=queue_name, exclusive=True)
        self._channel.queue_bind(exchange=self.EXCHANGE_NAME, queue=queue_name)

    def _consume_messages(self, queue_name):
        # noinspection PyUnusedLocal
        def callback(ch, method, properties, body):  # required signature for callback
            self._river.message(self, body.decode("utf-8"))
        self._channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        self._channel.start_consuming()
