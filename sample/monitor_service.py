# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import time
from rapidsrivers.packets.errors import PacketError
from rapidsrivers.rapids.rabbit_mq_rapids_connection import RabbitMqRapidsConnection
from rapidsrivers.validation.rules import Rules
from rapidsrivers.validation.validations import require_value, require_keys, forbid_keys


class Monitor:

    def __init__(self):
        self.name = '{0} [{1}]'.format('Monitor', hash(self))
        self.rules = Rules(
            # This requires Packet to have key-value pair
            # require_value('key_for_string', 'expectedValue'),
            # require_value('key_for_number', 42.42),
            #
            # This requires these keys exist (doesn't care about values)
            # require_keys('key1', 'key2', 'key3'),
            #
            # This forbids these keys existing. Note that 'null', empty string,
            # and empty arrays are considered to not exist
            # forbid_keys('key4', 'key5')
        )

    @staticmethod
    def main(*args):
        if len(args) != 2:
            raise PacketError('Missing IP and Port arguements! The IP address of the Rapids (as a string), '
                              'and the Port number of the Rapids (int or string).')
        rapids_connection = RabbitMqRapidsConnection(args[0], args[1])
        rapids_connection.register(Monitor())
        time.sleep(60 * 60 * 24)  # terminates in a day

    @staticmethod
    def packet(connection, packet, information):
        print(' [x] {0}'.format(information))

    @staticmethod
    def rejected_packet(connection, packet, problems):
        print(' [x] {0}'.format(problems))


if __name__ == '__main__':
    Monitor.main('localhost', 5672)
