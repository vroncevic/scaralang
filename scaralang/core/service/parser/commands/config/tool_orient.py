# -*- coding: UTF-8 -*-

'''
Module
    tool_orient.py
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
    Implementation of command parser parsing TOOL_ORIENT wrist 4th-axis orientation commands.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.token.token import ScaraToken
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.parameter.extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolOrientParser:
    '''
        Command parser handler for wrist tool orientation mode instructions.

        It defines:

            :attributes:
                | NAME - Component identification name.
                | MIN_TOKENS - Minimum allowed token count for statement parsing.
                | CMD_INDEX - Index of command token.
                | MODE_INDEX - Index of orientation mode token.
                | PARAMS_START_INDEX - Slice start index for key-value parameters.
                | VALID_MODES - Supported wrist tool orientation modes.
                | name - Property returning component name.
            :methods:
                | can_parse - Checks whether command is TOOL_ORIENT.
                | parse - Parses tool orient statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'tool_orient_parser'
    MIN_TOKENS: ClassVar[int] = 2
    CMD_INDEX: ClassVar[int] = 0
    MODE_INDEX: ClassVar[int] = 1
    PARAMS_START_INDEX: ClassVar[int] = 2
    VALID_MODES: ClassVar[tuple[ToolOrientMode, ToolOrientMode, ToolOrientMode]] = (
        ToolOrientMode.TANGENTIAL,
        ToolOrientMode.FIXED,
        ToolOrientMode.JOINT_LOCKED,
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
            Checks if command is TOOL_ORIENT.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name == ScaraCommandType.TOOL_ORIENT

    def parse(
        self,
        *,
        tokens: tuple[ScaraToken, ...],
        line_num: int,
        raw_text: str,
    ) -> ScaraInstruction:
        '''
            Parses tool orient statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
            :exceptions: ScaraSyntaxError on missing orientation mode.
        '''
        if len(tokens) < self.MIN_TOKENS:
            raise ScaraSyntaxError(
                f'Invalid TOOL_ORIENT syntax at line {line_num}. '
                'Expected: TOOL_ORIENT <TANGENTIAL|FIXED|JOINT_LOCKED>'
            )

        mode: str = tokens[self.MODE_INDEX].value.upper()

        if mode not in self.VALID_MODES:
            raise ScaraSyntaxError(
                f'Invalid tool orientation mode {mode!r} at line {line_num}. '
                'Expected TANGENTIAL, FIXED, or JOINT_LOCKED'
            )

        sub_params: dict[str, object] = ParameterExtractor.extract_key_values(
            tokens=tokens[self.PARAMS_START_INDEX:]
        )
        params: dict[str, object] = {ScaraInstructionParam.MODE: mode}

        if ScaraInstructionParam.PHI in sub_params:
            phi_val: object = sub_params[ScaraInstructionParam.PHI]
            params[ScaraInstructionParam.PHI] = phi_val

        return ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
