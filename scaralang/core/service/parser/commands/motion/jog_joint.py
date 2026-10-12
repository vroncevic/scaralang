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

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogJointParser:
    '''
        Command parser handler for manual jog instructions rotating robot joints.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is JOG_JOINT.
                | parse - Parses JOG_JOINT statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes JogJointParser.'''
        self._name: str = 'jog_joint_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is JOG_JOINT.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.JOG_JOINT

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
        cmd: str = tokens[0].value.upper()

        if len(tokens) < 3:
            raise ScaraSyntaxError(
                f'Invalid {cmd} syntax at line {line_num}. Expected: {cmd} <joint> <delta>'
            )

        try:
            joint_id: int = int(tokens[1].value)
            deg: float = float(tokens[2].value)

        except ValueError as exc:
            raise ScaraSyntaxError(
                f'Invalid JOG_JOINT arguments at line {line_num}. '
                'Expected integer joint ID and numeric degrees, got: '
                f'{tokens[1].value!r}, {tokens[2].value!r}'
            ) from exc

        return ScaraInstruction(
            command_type=ScaraCommandType.JOG_JOINT,
            line_number=line_num,
            raw_text=raw_text,
            parameters={
                InstructionParam.JOINT: joint_id,
                InstructionParam.DEG: deg,
            },
        )
