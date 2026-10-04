# -*- coding: UTF-8 -*-

'''
Module
    state_homing_validator_test.py
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
    Unit tests for StateHomingValidator operations.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext
from scaralang.core.service.linter.rules.state.state_homing_validator import StateHomingValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateHomingValidator(TestCase):
    '''
        Test cases verifying StateHomingValidator operations.

        It defines:

            :methods:
                | test_home_instruction_marks_homed - Verifies is_homed is set and coords cleared.
                | test_non_home_instruction_no_op - Verifies other instructions leave state unchanged.
                | test_name - Verifies validator name property.
    '''

    def test_home_instruction_marks_homed(self) -> None:
        '''
            Verifies HOME instruction sets is_homed to True and resets last_coords.
        '''
        validator = StateHomingValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        context = ScaraLintContext(
            is_homed=False,
            last_coords=(100.0, 50.0, 10.0, 0.0),
        )

        validator.validate(instruction=instruction, context=context)

        self.assertTrue(context.is_homed)
        self.assertEqual(context.last_coords, ())

    def test_non_home_instruction_no_op(self) -> None:
        '''
            Verifies non-HOME instruction does not alter homing state.
        '''
        validator = StateHomingValidator()
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=100.0',
            parameters={},
        )
        context = ScaraLintContext(
            is_homed=False,
            last_coords=(50.0, 50.0, 10.0, 0.0),
        )

        validator.validate(instruction=instruction, context=context)

        self.assertFalse(context.is_homed)
        self.assertEqual(context.last_coords, (50.0, 50.0, 10.0, 0.0))

    def test_name(self) -> None:
        '''
            Verifies validator name property.
        '''
        validator = StateHomingValidator()
        self.assertEqual(validator.name, 'state_homing')


if __name__ == '__main__':
    main()
