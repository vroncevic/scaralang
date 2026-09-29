# -*- coding: UTF-8 -*-

'''
Module
    elbow_config_parser.py
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
    Implementation of ICommandParser parsing CONFIG ELBOW configuration commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.kinematics.elbow_config import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ElbowConfigParser:
    '''
        Command parser handler for CONFIG ELBOW orientation instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is CONFIG or CONFIG_ELBOW.
                | parse - Parses CONFIG ELBOW statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes ElbowConfigParser.'''
        self._name: str = 'elbow_config_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is CONFIG or CONFIG_ELBOW.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            ScaraCommandType.CONFIG,
            ScaraCommandType.CONFIG_ELBOW,
        )

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses CONFIG ELBOW statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ValueError on invalid elbow configuration syntax.
        '''
        if len(tokens) < 3:
            raise ValueError(
                f'Invalid CONFIG syntax at line {line_num}. Expected: CONFIG ELBOW <LEFT|RIGHT>'
            )

        sub: str = tokens[1].value.upper()

        if sub != 'ELBOW':
            raise ValueError(
                f'Unknown CONFIG property {sub!r} at line {line_num}'
            )
        val: str = tokens[2].value.upper()

        if val not in (ElbowConfig.LEFT, ElbowConfig.RIGHT):
            raise ValueError(
                f'Invalid elbow configuration {val!r} at line {line_num}. Must be LEFT or RIGHT'
            )

        return ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_ELBOW,
            line_number=line_num,
            raw_text=raw_text,
            parameters={InstructionParam.ELBOW: val, 'elbow': val},
        )
