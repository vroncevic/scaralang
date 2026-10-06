# -*- coding: UTF-8 -*-

'''
Module
    command_type_test.py
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
    Unit tests for ScaraCommandType enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCommandTypeTest(TestCase):
    '''Unit tests validating ScaraCommandType enumeration members and string values.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined DSL commands.'''
        self.assertEqual(len(ScaraCommandType), 35)

    def test_string_representation(self) -> None:
        '''Verify that enum members equal their uppercase string names.'''
        self.assertEqual(ScaraCommandType.CONFIG, 'CONFIG')
        self.assertEqual(ScaraCommandType.CONFIG_MOTOR, 'CONFIG_MOTOR')
        self.assertEqual(ScaraCommandType.HOME, 'HOME')
        self.assertEqual(ScaraCommandType.MOVE_L, 'MOVE_L')
        self.assertEqual(ScaraCommandType.MOVE_J, 'MOVE_J')
        self.assertEqual(ScaraCommandType.SPEED, 'SPEED')
        self.assertEqual(ScaraCommandType.ESTOP, 'ESTOP')

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from string values.'''
        self.assertIs(ScaraCommandType('HOME'), ScaraCommandType.HOME)
        self.assertIs(ScaraCommandType('MOVE_L'), ScaraCommandType.MOVE_L)
        self.assertIs(ScaraCommandType('ENABLE'), ScaraCommandType.ENABLE)

    def test_invalid_command_raises_value_error(self) -> None:
        '''Verify that invalid command string raises ValueError.'''
        with self.assertRaises(ValueError):
            ScaraCommandType('INVALID_CMD')


if __name__ == '__main__':
    main()
