# -*- coding: UTF-8 -*-

'''
Module
    tool_id_test.py
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
    Unit tests for ToolId protocol enumeration model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.tool_id import ToolId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolIdTest(TestCase):
    '''Unit tests validating ToolId enumeration members, integer values, and lookups.'''

    def test_enumeration_members_count(self) -> None:
        '''Verify total number of defined end-effector tools.'''
        self.assertEqual(len(ToolId), 2)

    def test_tool_values(self) -> None:
        '''Verify integer identifiers for tool actuators.'''
        self.assertEqual(ToolId.PUMP, 0)
        self.assertEqual(ToolId.VALVE, 1)

    def test_lookup_by_value(self) -> None:
        '''Verify member lookup from integer values.'''
        self.assertIs(ToolId(0), ToolId.PUMP)
        self.assertIs(ToolId(1), ToolId.VALVE)

    def test_invalid_value_raises_value_error(self) -> None:
        '''Verify that undefined tool identifier raises ValueError.'''
        with self.assertRaises(ValueError):
            ToolId(99)


if __name__ == '__main__':
    main()
