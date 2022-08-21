# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.
#

from rapidsrivers.packets.errors import PacketError


def validate_service(service):
    if not hasattr(service, 'name'):
        raise PacketError('Service does not have a required "name" attribute')
    if not hasattr(service, 'rules'):
        raise PacketError('Service does not have a required "rules" attribute')
    if not hasattr(service, 'packet'):
        raise PacketError('Service does not have a required "packet" method')
