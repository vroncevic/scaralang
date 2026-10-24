# -*- coding: UTF-8 -*-

'''
Module
    elbow.py
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
    Implementation of command parser parsing CONFIG ELBOW configuration commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.model.kinematics.solver.elbow import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ElbowParser:
    '''
        Command parser handler for CONFIG ELBOW orientation instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | SUB_INDEX - Index of configuration property subcommand token.
                | VAL_INDEX - Index of configuration value token.
                | SUBCOMMAND_KEYWORD - Expected configuration property keyword.
                | VALID_CONFIGS - Supported elbow kinematic configuration modes.
                | PARSED_COMMANDS - Tuple of handled command keywords.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is CONFIG or CONFIG_ELBOW.
                | parse - Parses CONFIG ELBOW statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'elbow_parser'
    MIN_TOKENS: ClassVar[int] = 3
    CMD_INDEX: ClassVar[int] = 0
    SUB_INDEX: ClassVar[int] = 1
    VAL_INDEX: ClassVar[int] = 2
    SUBCOMMAND_KEYWORD: ClassVar[str] = 'ELBOW'
    VALID_CONFIGS: ClassVar[tuple[ElbowConfig, ElbowConfig]] = (
        ElbowConfig.LEFT,
        ElbowConfig.RIGHT,
    )
    PARSED_COMMANDS: ClassVar[tuple[ScaraCommandType, ScaraCommandType]] = (
        ScaraCommandType.CONFIG,
        ScaraCommandType.CONFIG_ELBOW,
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
            Checks if command is CONFIG or CONFIG_ELBOW.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in self.PARSED_COMMANDS

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
            :exceptions: ScaraSyntaxError on invalid elbow configuration syntax.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid CONFIG syntax at line {line_num}. Expected: CONFIG ELBOW <LEFT|RIGHT>'
            )

        sub: str = tokens[self.SUB_INDEX].value.upper()

        if sub != self.SUBCOMMAND_KEYWORD:
            raise ScaraSyntaxError(
                f'Unknown CONFIG property {sub!r} at line {line_num}'
            )

        val: str = tokens[self.VAL_INDEX].value.upper()

        if val not in self.VALID_CONFIGS:
            raise ScaraSyntaxError(
                f'Invalid elbow configuration {val!r} at line {line_num}. Must be LEFT or RIGHT'
            )

        return ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_ELBOW,
            line_number=line_num,
            raw_text=raw_text,
            parameters={ScaraInstructionParam.ELBOW: val},
        )
