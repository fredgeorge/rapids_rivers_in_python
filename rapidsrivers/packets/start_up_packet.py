# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import json

from rapidsrivers.packets.constants import *


class StartUpPacket:

    def __init__(self, service):
        self._service_name = service.name

    def to_json_string(self):
        return json.dumps({
            COMMUNITY_KEY : SYSTEM_COMMUNITY_VALUE,
            PACKET_TYPE_KEY: SYSTEM_PACKET_TYPE_VALUE,
            SYSTEM_PURPOSE_KEY : START_UP_SYSTEM_PURPOSE_VALUE,
            SERVICE_NAME_KEY: self._service_name
        })

    def __str__(self):
        return self.to_json_string()
