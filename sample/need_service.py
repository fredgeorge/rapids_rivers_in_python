# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json
import time

from rapidsrivers.packets.constants import COMMUNITY_KEY
from rapidsrivers.packets.errors import PacketError
from rapidsrivers.rapids.rabbit_mq_rapids_connection import RabbitMqRapidsConnection


class Need:

    OFFER_ENGINE_COMMUNITY_VALUE = 'offer_engine_family'
    NEED_KEY = 'need'
    CAR_RENTAL_OFFER_NEED_VALUE = 'car_rental_offer'

    @staticmethod
    def main(*args):
        if len(args) != 2:
            raise PacketError('Missing IP and Port arguements! The IP address of the Rapids (as a string), '
                              'and the Port number of the Rapids (int or string).')
        rapids_connection = RabbitMqRapidsConnection(args[0], args[1])
        need_packet = json.dumps({
                    COMMUNITY_KEY: Need.OFFER_ENGINE_COMMUNITY_VALUE,
                    Need.NEED_KEY: Need.CAR_RENTAL_OFFER_NEED_VALUE
                })
        while True:
            print(' [<] {0}'.format(need_packet))
            rapids_connection.publish(need_packet)
            time.sleep(5)

    def _need(self):
        return


if __name__ == '__main__':
    Need.main('localhost', 5672)
