# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.


class SampleService:

    def __init__(self, rules):
        self.name = 'SampleService [{0}]'.format(hash(self))
        self.rules = rules
        self.accepted_packets = []
        self.rejected_packets = []
        self.information_statuses = []
        self.problem_statuses = []

    def packet(self, connection, packet, information):
        self.accepted_packets.append(packet)
        self.information_statuses.append(information)

    def rejected_packet(self, connection, packet, problems):
        self.rejected_packets.append(packet)
        self.problem_statuses.append(problems)
