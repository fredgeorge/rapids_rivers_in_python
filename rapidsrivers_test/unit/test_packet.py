# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import pytest
from _datetime import datetime

from rapidsrivers.packets.errors import PacketError
from rapidsrivers.packets.packet import Packet


class TestPacket:
    _jsonString = '''
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
    '''

    def test_fetch_nugget(self):
        _packet = Packet(self._jsonString)
        assert 'rental_offer_engine' == _packet['string_key']
        assert 7 == _packet['integer_key']
        assert 7.0 == _packet['integer_key']
        assert 7.5 == _packet['double_key']
        assert _packet['boolean_key']
        assert datetime(2022, 3, 3) == _packet.date('date_time_key')
        assert 'upgrade' == _packet['detail_key']['detail_string_key']
        assert _packet.has('detail_key')
        assert 10.75 == _packet['detail_key']['detail_double_key']

    def test_is_missing(self):
        _packet = Packet(self._jsonString)
        assert _packet.is_lacking('foo')
        assert _packet.is_lacking('empty')
        assert _packet.is_lacking('null_key')
        assert _packet.is_lacking('empty_list_key')

    def test_invalid_json(self):
        with pytest.raises(PacketError):
            Packet('{')
        with pytest.raises(PacketError):
            Packet('')

    def test_extraction_problem(self):
        _packet = Packet(self._jsonString)
        with pytest.raises(PacketError):
            _packet.date('string_key')
