# Copyright (c) 2022 by Fred George
# @author Fred George  fredgeorge@acm.org
# Licensed under the MIT License; see LICENSE file in root.


class Status:

    def __init__(self, original_json_string):
        self._json_string = original_json_string
        self._information_messages = []
        self._error_messages = []

    def has_errors(self):
        return len(self._error_messages) > 0

    def unexpectedly_missing(self, key):
        self._error_messages.append('Required key of <{0}> is missing'.format(key))

    def found_expected(self, key):
        self._information_messages.append('Required key of <{0}> was found'.format(key))

    def unexpectedly_found(self, key):
        self._error_messages.append('Forbidden key of <{0}> unexpectedly exists'.format(key))

    def missing_expected(self, key):
        self._information_messages.append('Forbidden key of <{0}> was not found'.format(key))
