# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

from rapidsrivers.validation.rules import Rules
from rapidsrivers_test.util.sample_rapids_connection import SampleRapidsConnection
from rapidsrivers_test.util.sample_services import SampleService


class TestRiver:

    _json_string = '''
        {
            "string_key":"rental_offer_engine",
            "integer_key":7,
            "double_key":7.5,
            "boolean_key": true,
            "date_time_key": "2022-03-03T00:00:00Z",
            "string_list_key":["foo","bar"],
            "integer_list_key":[2,4],
            "detail_key":{
                "detail_string_key":"upgrade",
                "detail_double_key":10.75
            }
        }
    '''

    def test_unfiltered_service(self):
        connection = SampleRapidsConnection(2)
        service = SampleService(Rules())
        connection.register(service)
        assert len(connection.all_packets) == 1