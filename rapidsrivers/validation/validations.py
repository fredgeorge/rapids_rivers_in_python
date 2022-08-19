# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

def require_keys(*keys):
    return [_RequireKey(key) for key in keys]

class _RequireKey:
    def __init__(self, key):
        self._key = key

    def _evaluate(self, packet, status):
        if packet.is_missing(self._key):
            status._unexpectedly_missing(self._key)
        else:
            status._found_expected(self._key)
