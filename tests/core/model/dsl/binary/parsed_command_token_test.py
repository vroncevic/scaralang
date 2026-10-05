# -*- coding: UTF-8 -*-

'''
Module
    parsed_command_token_test.py
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
    Unit tests for ParsedCommandToken domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.parsed_command_token import ParsedCommandToken

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParsedCommandToken(TestCase):
    '''
        Test cases verifying ParsedCommandToken immutability and attributes.

        It defines:

            :methods:
                | test_initialization - Verifies attributes assignment.
                | test_immutability - Verifies frozen dataclass behavior.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attributes initialization on ParsedCommandToken.
        '''
        token = ParsedCommandToken(
            cmd_name='WAIT',
            arg='100',
            clean='<CMD:WAIT#100>',
            parts=('WAIT', '100'),
        )
        self.assertEqual(token.cmd_name, 'WAIT')
        self.assertEqual(token.arg, '100')
        self.assertEqual(token.clean, '<CMD:WAIT#100>')
        self.assertEqual(token.parts, ('WAIT', '100'))

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass rejects attribute mutations.
        '''
        token = ParsedCommandToken(
            cmd_name='HOME',
            arg='',
            clean='<CMD:HOME>',
        )
        with self.assertRaises(FrozenInstanceError if 'FrozenInstanceError' in globals() else Exception):
            token.cmd_name = 'HOLD'  # type: ignore[misc]


if __name__ == '__main__':
    main()
