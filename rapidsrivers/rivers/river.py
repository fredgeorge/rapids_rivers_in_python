# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
from rapidsrivers.packets.packet import Packet
from rapidsrivers.packets.start_up_packet import StartUpPacket


class River:

    def __init__(self, connection, rules, max_read_count):
        self._connection = connection
        self._rules = rules
        self._max_read_count = max_read_count
        self._listeners = []
        self._system_listeners = []

    def register(self, service):
        self._listeners.append(service)
        if hasattr(service, 'is_system_service') and service.is_system_service is True:
            self._system_listeners.append(service)
        self._connection.publish(StartUpPacket(service))

    def message(self, connection, message):
        packet = Packet(message)
        status = packet.evaluate(self._rules)
        if status.has_errors():
            self._trigger_rejected_packet(connection, packet, status)
        else:
            self._trigger_accepted_packet(connection, packet, status)

    def _trigger_accepted_packet(self, connection, packet, status):
        for service in self._listeners:
            service.packet(connection, packet, status)

    def _trigger_rejected_packet(self, connection, packet, status):
        for service in self._listeners:
            if hasattr(service, 'rejected_packet'):
                service.rejected_packet(connection, packet, status)
