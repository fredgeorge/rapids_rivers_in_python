# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

def require_keys(*keys):
    return [_RequireKey(key) for key in keys]


class _RequireKey:
    def __init__(self, key):
        self._key = key

    def _evaluate(self, packet, status):
        if packet.is_lacking(self._key):
            status.unexpectedly_missing(self._key)
        else:
            status.found_expected(self._key)


def forbid_keys(*keys):
    return [_ForbidKey(key) for key in keys]


class _ForbidKey:
    def __init__(self, key):
        self._key = key

    def _evaluate(self, packet, status):
        if packet.is_lacking(self._key):
            status.missing_expected(self._key)
        else:
            status.unexpectedly_found(self._key)
