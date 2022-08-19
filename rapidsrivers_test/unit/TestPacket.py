# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import pytest
from _datetime import datetime
from rapidsrivers.packet.packet import Packet


class TestPacket:

    _packet = Packet('''
        {
            "string_key":"rental_offer_engine",
            "integer_key":7,
            "double_key":7.5,
            "null_key":null,
            "empty_string":"",
            "boolean_key": true,
            "boolean_string_key": "false",
            "date_time_key": "2022-03-03T00:00:00Z",
            "string_list_key":["foo","bar"],
            "integer_list_key":[2,4],
            "empty_list_key":[],
            "detail_key":{
                "detail_string_key":"upgrade",
                "detail_double_key":10.75
            }
        }
    ''')

    def test_fetch_nugget(self):
        assert 'rental_offer_engine' == self._packet['string_key']
        assert 7 == self._packet['integer_key']
        assert 7.0 == self._packet['integer_key']
        assert 7.5 == self._packet['double_key']
        assert self._packet['boolean_key']
        assert datetime(2022, 3, 3) == self._packet.date('date_time_key')
