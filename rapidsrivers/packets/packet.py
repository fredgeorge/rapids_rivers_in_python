# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json
from datetime import datetime
from json import JSONDecodeError

from rapidsrivers.packets.errors import PacketError
from rapidsrivers.rivers.status import Status


class Packet:
    def __init__(self, raw_json_string):
        self._json_string = raw_json_string
        try:
            self._map = json.loads(raw_json_string)
        except JSONDecodeError:
            raise PacketError('message')

    def __getitem__(self, item):
        return self._map[item]

    def date(self, date_time_key):
        try:
            return datetime.strptime(self._map[date_time_key], '%Y-%m-%dT%H:%M:%SZ')
        except(ValueError):
            raise PacketError('Key <{0}> is not in UTC date format'.format(date_time_key))

    def is_lacking(self, key):
        return key not in self._map or self._map[key] is None or self._map[key] == "" or self._map[key] == []

    def has(self, key):
        return not self.is_lacking(key)

    def evaluate(self, rules):
        status = Status(self._json_string)
        for rule in rules:
            rule._evaluate(self, status)
        return status

    def to_json_string(self):
        return json.dumps(self._map)

    def __str__(self):
        return self.to_json_string()
