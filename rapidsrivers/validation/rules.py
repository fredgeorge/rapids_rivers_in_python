# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.

class Rules:
    def __init__(self, *rules):
        self._rules = [rule for sublist in rules for rule in sublist] # Wierd flatten syntax

    def __iter__(self):
        return iter(self._rules)
