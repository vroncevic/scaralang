# -*- coding: UTF-8 -*-

'''
Module
    tool_orient_mode_test.py
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
    Unit testing for ToolOrientMode enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolOrientModeTest(TestCase):
    '''
        Validates member values and string equality of ToolOrientMode enumeration.
    '''

    def test_members(self) -> None:
        '''
            Verifies all enumeration members and their exact string representations.
        '''
        self.assertEqual(ToolOrientMode.FIXED, 'FIXED')
        self.assertEqual(ToolOrientMode.TANGENTIAL, 'TANGENTIAL')
        self.assertEqual(ToolOrientMode.JOINT_LOCKED, 'JOINT_LOCKED')
        self.assertEqual(len(ToolOrientMode), 3)

    def test_value_instantiation(self) -> None:
        '''
            Verifies instantiation from string literals.
        '''
        self.assertIs(ToolOrientMode('FIXED'), ToolOrientMode.FIXED)
        self.assertIs(ToolOrientMode('TANGENTIAL'), ToolOrientMode.TANGENTIAL)
        self.assertIs(ToolOrientMode('JOINT_LOCKED'), ToolOrientMode.JOINT_LOCKED)


if __name__ == '__main__':
    main()
