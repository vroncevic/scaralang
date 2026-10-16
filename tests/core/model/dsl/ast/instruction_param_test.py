# -*- coding: UTF-8 -*-

'''
Module
    instruction_param_test.py
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
    Unit tests for ScaraInstructionParam enumeration.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionParamTest(TestCase):
    '''Unit tests validating ScaraInstructionParam enumeration values.'''

    def test_members_count(self) -> None:
        '''Verify that 45 instruction parameter keys are defined.'''
        self.assertEqual(len(ScaraInstructionParam), 45)

    def test_member_string_values(self) -> None:
        '''Verify that members match their exact uppercase string values.'''
        self.assertEqual(ScaraInstructionParam.X, 'X')
        self.assertEqual(ScaraInstructionParam.Y, 'Y')
        self.assertEqual(ScaraInstructionParam.Z, 'Z')
        self.assertEqual(ScaraInstructionParam.PHI, 'PHI')
        self.assertEqual(ScaraInstructionParam.SPEED, 'SPEED')
        self.assertEqual(ScaraInstructionParam.MODE, 'MODE')
        self.assertEqual(ScaraInstructionParam.MOTOR_MODE, 'MOTOR_MODE')
        self.assertEqual(ScaraInstructionParam.INTERFACE, 'INTERFACE')
        self.assertEqual(ScaraInstructionParam.AXIS_MASK, 'AXIS_MASK')
        self.assertEqual(ScaraInstructionParam.STATE, 'STATE')
        self.assertEqual(ScaraInstructionParam.DIST, 'DIST')
        self.assertEqual(ScaraInstructionParam.ANGLE, 'ANGLE')
        self.assertEqual(ScaraInstructionParam.ARCH, 'ARCH')

    def test_lookup_by_value(self) -> None:
        '''Verify string lookup returns matching enum instance.'''
        self.assertIs(
            ScaraInstructionParam('SPEED'),
            ScaraInstructionParam.SPEED,
        )


if __name__ == '__main__':
    main()
