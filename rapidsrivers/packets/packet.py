# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json
from datetime import datetime
from json import JSONDecodeError

from rapidsrivers.packets.constants import *
from rapidsrivers.packets.errors import PacketError
from rapidsrivers.packets.heart_beat_packet import HeartBeat
from rapidsrivers.rivers.status import Status


class Packet:
    def __init__(self, raw_json_string):
        self._json_string = raw_json_string
        try:
            self._map = json.loads(raw_json_string)
        except JSONDecodeError:
            raise PacketError('message')

    @staticmethod
    def empty():
        return Packet('{}')

    def __getitem__(self, item):
        return self._map[item]

    def __setitem__(self, key, value):
        self._map[key] = value

    def date(self, date_time_key):
        try:
            return datetime.strptime(self._map[date_time_key], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            raise PacketError('Key <{0}> is not in UTC date format'.format(date_time_key))

    def is_lacking(self, key):
        return key not in self._map or self._map[key] is None or self._map[key] == "" or self._map[key] == []

    def has(self, key):
        return not self.is_lacking(key)

    def is_system(self):
        return self.has(PACKET_TYPE_KEY) and \
               self._map[PACKET_TYPE_KEY] == SYSTEM_PACKET_TYPE_VALUE

    def is_heart_beat(self):
        return not self.evaluate(HeartBeat.rules()).has_errors()

    def to_heart_beat_response(self, service):
        response = Packet(self._json_string)  # clone the packet
        response[HEART_BEAT_RESPONDER_KEY] = service.name
        return response

    def has_invalid_read_count(self, max_read_count):
        return max_read_count != 0 and self._system_read_count() > max_read_count

    def _system_read_count(self):
        result = 1 if self.is_lacking(SYSTEM_READ_COUNT_KEY) else self[SYSTEM_READ_COUNT_KEY] + 1
        self[SYSTEM_READ_COUNT_KEY] = result
        return result

    def evaluate(self, rules):
        status = Status(self._json_string)
        for rule in rules:
            rule.evaluate(self, status)
        return status

    def to_json_string(self):
        return json.dumps(self._map)

    def __str__(self):
        return self.to_json_string()
