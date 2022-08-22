# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json

from rapidsrivers.packets.constants import *
from rapidsrivers.validation.rules import Rules
from rapidsrivers.validation.validations import require_value, require_keys, forbid_keys


class HeartBeat:

    def __init__(self):
        self._index = 0

    @staticmethod
    def rules():
        return Rules(
            require_value(COMMUNITY_KEY, SYSTEM_COMMUNITY_VALUE),
            require_value(PACKET_TYPE_KEY, SYSTEM_PACKET_TYPE_VALUE),
            require_value(SYSTEM_PURPOSE_KEY, HEART_BEAT_SYSTEM_PURPOSE_VALUE),
            require_keys(HEART_BEAT_GENERATOR_KEY, HEART_BEAT_INDEX_KEY),
            forbid_keys(HEART_BEAT_RESPONDER_KEY)
        )

    def to_json_string(self):
        self._index += 1
        return self._json_string()

    def _json_string(self):
        return json.dumps({
            COMMUNITY_KEY : SYSTEM_COMMUNITY_VALUE,
            PACKET_TYPE_KEY: SYSTEM_PACKET_TYPE_VALUE,
            SYSTEM_PURPOSE_KEY : HEART_BEAT_SYSTEM_PURPOSE_VALUE,
            HEART_BEAT_GENERATOR_KEY: hash(self),
            HEART_BEAT_INDEX_KEY: self._index
        })

    def __str__(self):
        return self._json_string()
