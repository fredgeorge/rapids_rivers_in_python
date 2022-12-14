# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

import pytest

from rapidsrivers.packets.packet import Packet
from rapidsrivers.validation.rules import Rules
from rapidsrivers.validation.validations import require_keys, forbid_keys, require_value


class TestValidation:
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

    def test_no_rules(self):
        self._assert_passes(Rules())

    def test_required_keys(self):
        self._assert_passes(Rules(require_keys('string_key', 'integer_key')))
        self._assert_fails(Rules(require_keys('string_key', 'foo')))
        self._assert_passes(Rules(require_keys('detail_key')))

    def test_forbidden_key(self):
        self._assert_passes(Rules(forbid_keys('foo')))
        self._assert_fails(Rules(forbid_keys('string_key', 'foo')))
        self._assert_passes(Rules(forbid_keys('null_key', 'empty_string', 'empty_list_key')))

    def test_require_specific_string(self):
        self._assert_passes(Rules(require_value('string_key', 'rental_offer_engine')))
        self._assert_fails(Rules(require_value('string_key', 'foo')))
        self._assert_fails(Rules(require_value('bar', 'foo')))

    def test_require_specific_number(self):
        self._assert_passes(Rules(require_value('integer_key', 7)))
        self._assert_passes(Rules(require_value('integer_key', 7.0)))
        self._assert_fails(Rules(require_value('integer_key', 8)))
        self._assert_passes(Rules(require_value('double_key', 7.5)))
        self._assert_fails(Rules(require_value('double_key', 8)))

    def test_require_specific_boolean(self):
        self._assert_passes(Rules(require_value('boolean_key', True)))
        self._assert_fails(Rules(require_value('boolean_key', False)))
        self._assert_fails(Rules(require_value('boolean_string_key', 'true')))
        self._assert_passes(Rules(require_value('boolean_string_key', 'false')))
        self._assert_fails(Rules(require_value('boolean_string_key', False))) # must use quoted value

    def test_compound_rules(self):
        self._assert_passes(Rules(
            require_keys('string_key', 'integer_key'),
            require_value('boolean_key', True),
            forbid_keys('null_key', 'empty_string', 'empty_list_key'),
            require_keys('detail_key', 'boolean_string_key')
        ))

    def _assert_passes(self, rules):
        status = Packet(self._jsonString).evaluate(rules)
        assert not status.has_errors()

    def _assert_fails(self, rules):
        status = Packet(self._jsonString).evaluate(rules)
        assert status.has_errors()
