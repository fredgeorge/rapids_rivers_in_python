# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
from rapidsrivers.packets.packet import Packet
from rapidsrivers.validation.rules import Rules
from rapidsrivers.validation.validations import require_keys, forbid_keys
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
        packet = Packet(self._json_string)
        service = SampleService(Rules())
        connection.register(service)
        connection.publish(packet)
        assert len(service.accepted_packets) == 1
        assert len(service.information_statuses) == 1
        assert len(service.rejected_packets) == 0
        assert len(service.problem_statuses) == 0

    def test_filtered_service(self):
        connection = SampleRapidsConnection(2)
        packet = Packet(self._json_string)
        accepted_service = SampleService(Rules(require_keys('integer_key')))
        rejected_service = SampleService(Rules(forbid_keys('integer_key')))
        connection.register(accepted_service)
        connection.register(rejected_service)
        connection.publish(packet)
        assert len(accepted_service.accepted_packets) == 1
        assert accepted_service.information_statuses[0].has_errors() is False
        assert len(rejected_service.rejected_packets) == 1
        assert rejected_service.problem_statuses[0].has_errors() is True

    def test_start_up_packet(self):
        connection = SampleRapidsConnection(2)
        service = SampleService(Rules())
        connection.register(service)
        assert len(connection.all_packets) == 1
