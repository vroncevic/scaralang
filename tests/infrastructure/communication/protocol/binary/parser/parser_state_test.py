# -*- coding: UTF-8 -*-

'''
Module
    parser_state_test.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scaralang is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scaralang is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Unit tests for ParserState enumeration.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.communication.protocol.binary.parser.parser_state import ParserState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParserState(TestCase):
    '''
        Test cases verifying ParserState enumeration.

        It defines:

            :methods:
                | test_parser_state_enums - Verifies integer values of ParserState enum.
    '''

    def test_parser_state_enums(self) -> None:
        '''
            Tests parser state machine enum values.
        '''
        self.assertEqual(int(ParserState.SEARCH_SOF1), 0)
        self.assertEqual(int(ParserState.SEARCH_SOF2), 1)
        self.assertEqual(int(ParserState.READ_MSG_ID), 2)
        self.assertEqual(int(ParserState.READ_SEQ_NUM), 3)
        self.assertEqual(int(ParserState.READ_PAYLOAD_LEN), 4)
        self.assertEqual(int(ParserState.READ_PAYLOAD), 5)
        self.assertEqual(int(ParserState.READ_CRC_LO), 6)
        self.assertEqual(int(ParserState.READ_CRC_HI), 7)
        self.assertEqual(int(ParserState.READ_EOF), 8)


if __name__ == '__main__':
    main()
