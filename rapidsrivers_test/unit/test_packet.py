# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import pytest
from _datetime import datetime

from rapidsrivers.packet.errors import PacketError
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
        assert 'upgrade' == self._packet['detail_key']['detail_string_key']
        assert 10.75 == self._packet['detail_key']['detail_double_key']

    def test_is_missing(self):
        assert self._packet.is_missing('foo')
        assert self._packet.is_missing('empty')
        assert self._packet.is_missing('null_key')
        assert self._packet.is_missing('empty_list_key')

    def test_invalid_json(self):
        with pytest.raises(PacketError):
            Packet('{')
        with pytest.raises(PacketError):
            Packet('')

    def test_extraction_problem(self):
        with pytest.raises(PacketError):
            self._packet.date('string_key')