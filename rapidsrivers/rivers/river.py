# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

from rapidsrivers.packets.constants import *
from rapidsrivers.packets.errors import PacketError
from rapidsrivers.packets.packet import Packet
from rapidsrivers.packets.start_up_packet import StartUpPacket
from rapidsrivers.rivers.status import Status


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
        try:
            packet = Packet(message)
            if packet.has_invalid_read_count(self._max_read_count):
                self._trigger_loop_detection(connection, packet)
                return
            if packet.is_heart_beat():
                self._trigger_heart_beat_response(connection, packet)
            status = packet.evaluate(self._rules)
            listeners = self._system_listeners if packet.is_system() else self._listeners
            if status.has_errors():
                self._trigger_rejected_packet(listeners, connection, packet, status)
            else:
                self._trigger_accepted_packet(listeners, connection, packet, status)
        except PacketError as err:
            self._trigger_invalid_format(connection, message, err)

    @staticmethod
    def _trigger_accepted_packet(listeners, connection, packet, status):
        breadcrumbs = [] if packet.is_lacking(SYSTEM_BREADCRUMBS_KEY) else packet[SYSTEM_BREADCRUMBS_KEY]
        for service in listeners:
            packet[SYSTEM_BREADCRUMBS_KEY] = breadcrumbs + [service.name]
            service.packet(connection, packet, status)

    @staticmethod
    def _trigger_rejected_packet(listeners, connection, packet, status):
        for service in listeners:
            if hasattr(service, 'rejected_packet'):
                service.rejected_packet(connection, packet, status)

    def _trigger_invalid_format(self, connection, message, error):
        status = Status(message)
        status.error(error)
        for service in self._system_listeners:
            if hasattr(service, 'invalid_format'):
                service.invalid_format(connection, message, status)

    def _trigger_heart_beat_response(self, connection, packet):
        for service in self._listeners:
            if not hasattr(service, 'is_still_alive') or service.is_still_alive(connection) is True:
                connection.publish(packet.to_heart_beat_response(service))

    def _trigger_loop_detection(self, connection, packet):
        for service in self._system_listeners:
            if hasattr(service, 'loop_detected'):
                service.loop_detected(connection, packet)
