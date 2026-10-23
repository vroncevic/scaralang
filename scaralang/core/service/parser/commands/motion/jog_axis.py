# -*- coding: UTF-8 -*-

'''
Module
    jog_axis.py
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
    Implementation of command parser parsing manual Cartesian JOG_AXIS instructions.
'''

from __future__ import annotations
from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.jog_axis import JogAxis
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogAxisParser:
    '''
        Command parser handler for manual jog instructions along Cartesian axes.

        It defines:

            :cvar NAME: Component identification name.
            :cvar MIN_TOKENS: Minimum required tokens for JOG_AXIS instruction.
            :cvar CMD_INDEX: Index of command token in sequence.
            :cvar AXIS_INDEX: Index of Cartesian axis name argument.
            :cvar VAL_INDEX: Index of jog step delta value argument.
            :cvar PARSED_COMMAND: Target command keyword string.
            :cvar VALID_AXES: Allowed Cartesian axes tuple.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is JOG_AXIS.
                | parse - Parses JOG_AXIS statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'jog_axis_parser'
    MIN_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    AXIS_INDEX: ClassVar[int] = 1
    VAL_INDEX: ClassVar[int] = 2
    PARSED_COMMAND: ClassVar[str] = ScaraCommandType.JOG_AXIS
    VALID_AXES: ClassVar[tuple[str, ...]] = (
        JogAxis.X,
        JogAxis.Y,
        JogAxis.Z,
        JogAxis.PHI,
    )

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is JOG_AXIS.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == self.PARSED_COMMAND

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses JOG_AXIS statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing or invalid jog axis arguments.
        '''
        cmd: str = tokens[self.CMD_INDEX].value.upper()

        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid {cmd} syntax at line {line_num}. Expected: {cmd} <axis> <delta>'
            )

        axis: str = tokens[self.AXIS_INDEX].value.upper()

        if axis not in self.VALID_AXES:
            raise ScaraSyntaxError(
                f'Invalid jog axis {axis!r} at line {line_num}. '
                'Expected X, Y, Z, or PHI'
            )

        try:
            step: float = float(tokens[self.VAL_INDEX].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid jog step delta {tokens[self.VAL_INDEX].value!r} at line {line_num}. '
                'Must be a valid number'
            ) from exc

        return ScaraInstruction(
            command_type=self.PARSED_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                ScaraInstructionParam.AXIS: axis,
                ScaraInstructionParam.STEP: step,
            },
        )
