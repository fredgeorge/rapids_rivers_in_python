# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json
from rapidsrivers.packet.errors import PacketError


class Packet:
    def __init__(self, raw_json_string):
        self._json_string = raw_json_string
        try:
            self._map = json.loads(raw_json_string)
        except RuntimeError:
            raise PacketError('message')

    def __getitem__(self, item):
        return self._map[item]