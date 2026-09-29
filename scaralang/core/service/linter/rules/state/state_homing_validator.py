# -*- coding: UTF-8 -*-

'''
Module
    state_homing_validator.py
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
    Updates homing calibration state and resets prior move coordinates.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.linter.scara_lint_context import ScaraLintContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StateHomingValidator:
    '''
        Updates context homing flags when encountering HOME instructions.

        It defines:

            :methods:
                | name - Returns validator identifier name.
                | validate - Marks context as homed and clears previous move coordinates.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the validator identifier name.

            :return: Validator identifier name string.
            :exceptions: None.
        '''
        return 'state_homing'

    def validate(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraLintContext,
    ) -> None:
        '''
            Applies homing state updates to simulation context.

            :param instruction: Primitive AST instruction node.
            :param context: Simulation lint context.
            :exceptions: None.
        '''
        if instruction.command_type == ScaraCommandType.HOME:
            context.is_homed = True
            context.last_coords = ()
