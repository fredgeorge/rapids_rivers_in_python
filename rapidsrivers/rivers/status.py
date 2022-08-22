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

    def error(self, message):
        self._error_messages.append(message)

    def unexpectedly_missing(self, key):
        self._error_messages.append('Required key of <{0}> is missing'.format(key))

    def found_expected(self, key):
        self._information_messages.append('Required key of <{0}> was found'.format(key))

    def unexpectedly_found(self, key):
        self._error_messages.append('Forbidden key of <{0}> unexpectedly exists'.format(key))

    def missing_expected(self, key):
        self._information_messages.append('Forbidden key of <{0}> was not found'.format(key))

    def missing_value(self, key, value):
        self._error_messages.append('Required key of <{0}> is missing required value of <{1}>'.format(key, value))

    def found_value(self, key, value):
        self._information_messages.append('Require key <{0}> has value <{1}>'.format(key, value))

    def __str__(self):
        result = 'Status of filtering of:\n'
        result += '\tOriginal packet: {0}\n'.format(self._json_string)
        result += self._details('Errors', self._error_messages)
        result += self._details('Informational messages', self._information_messages)
        return result

    @staticmethod
    def _details(category, messages):
        if len(messages) == 0:
            return ''
        result = '\t{0} - {1}:'.format(category, len(messages))
        for m in messages:
            result += '\t\t{0}\n'.format(m)
        return result
