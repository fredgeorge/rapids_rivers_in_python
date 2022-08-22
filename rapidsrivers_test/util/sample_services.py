# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
from rapidsrivers.validation.rules import Rules


class SampleService:

    def __init__(self, rules, is_system_service=False):
        self.name = 'SampleService [{0}]'.format(hash(self))
        self.rules = rules
        self.is_system_service = is_system_service
        self.accepted_packets = []
        self.rejected_packets = []
        self.information_statuses = []
        self.problem_statuses = []
        self.format_problems = []
        self.loop_packets = []

    def packet(self, connection, packet, information):
        self.accepted_packets.append(packet)
        self.information_statuses.append(information)

    def rejected_packet(self, connection, packet, problems):
        self.rejected_packets.append(packet)
        self.problem_statuses.append(problems)

    def invalid_format(self, connection, message, problems):
        self.format_problems.append(problems)

    def loop_detected(self, connection, packet):
        self.loop_packets.append(packet)


class DeadService(SampleService):

    def __init__(self):
        super().__init__(Rules())

    @staticmethod
    def is_still_alive(connection):
        return False


