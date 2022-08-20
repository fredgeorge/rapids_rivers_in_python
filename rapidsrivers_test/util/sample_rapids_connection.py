# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
from rapidsrivers.packets.errors import PacketError
from rapidsrivers.rivers.river import River


class SampleRapidsConnection:

    def __init__(self, max_read_count):
        self._max_read_count = max_read_count
        self._rivers = []
        self._messages = []
        self.all_packets = []
        self.all_messages = []

    def register(self, service):
        if not hasattr(service, 'name'):
            raise PacketError('Service does not have a required "name" attribute')
        if not hasattr(service, 'rules'):
            raise PacketError('Service does not have a required "rules" attribute')
        if not hasattr(service, 'packet'):
            raise PacketError('Service does not have a required "packet" method')
        river = River(self, service.rules, self._max_read_count)
        river.register(service)
        self._rivers.append(river)

    def publish(self, message_or_packet):
        is_packet = hasattr(message_or_packet, 'to_json_string')
        if is_packet:
            self.all_packets.append(message_or_packet)
        message = message_or_packet if not is_packet else message_or_packet.to_json_string()
        self.all_messages.append(message)
        if len(self._messages) > 0:
            self._messages.append(message)
        else:
            self._messages.append(message)
            while len(self._messages) > 0:
                next_message = self._messages[0]
                for river in self._rivers:
                    river.message(self, next_message)
                self._messages.pop(0)

