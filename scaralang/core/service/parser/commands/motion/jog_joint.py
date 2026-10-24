# -*- coding: UTF-8 -*-

'''
Module
    jog_joint.py
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
    Implementation of command parser parsing manual joint rotation JOG_JOINT instructions.
'''

from __future__ import annotations
from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogJointParser:
    '''
        Command parser handler for manual jog instructions rotating robot joints.

        It defines:

            :cvar NAME: Component identification name.
            :cvar MIN_TOKENS: Minimum required tokens for JOG_JOINT instruction.
            :cvar CMD_INDEX: Index of command token in sequence.
            :cvar JOINT_INDEX: Index of joint ID argument.
            :cvar VAL_INDEX: Index of degree rotation value argument.
            :cvar PARSED_COMMAND: Target command keyword string.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is JOG_JOINT.
                | parse - Parses JOG_JOINT statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'jog_joint_parser'
    MIN_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    JOINT_INDEX: ClassVar[int] = 1
    VAL_INDEX: ClassVar[int] = 2
    PARSED_COMMAND: ClassVar[str] = ScaraCommandType.JOG_JOINT

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is JOG_JOINT.

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
            Parses JOG_JOINT statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing or invalid jog joint arguments.
        '''
        cmd: str = tokens[self.CMD_INDEX].value.upper()

        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid {cmd} syntax at line {line_num}. Expected: {cmd} <joint> <delta>'
            )

        try:
            joint_id: int = int(tokens[self.JOINT_INDEX].value)
            deg: float = float(tokens[self.VAL_INDEX].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid JOG_JOINT arguments at line {line_num}. '
                'Expected integer joint ID and numeric degrees, got: '
                f'{tokens[self.JOINT_INDEX].value!r}, {tokens[self.VAL_INDEX].value!r}'
            ) from exc

        return ScaraInstruction(
            command_type=self.PARSED_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                ScaraInstructionParam.JOINT: joint_id,
                ScaraInstructionParam.DEG: deg,
            },
        )
