# -*- coding: UTF-8 -*-

'''
Module
    tool_orient_command_parser.py
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
    Implementation of ICommandParser parsing TOOL_ORIENT wrist 4th-axis orientation commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.parser.commands.parameter.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolOrientCommandParser:
    '''
        Command parser handler for wrist tool orientation mode instructions.

        It defines:

            :attributes:
                | _name - Component identification name.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is TOOL_ORIENT.
                | parse - Parses tool orient statement tokens into ScaraInstruction.
    '''

    def __init__(self) -> None:
        '''Initializes ToolOrientCommandParser.'''
        self._name: str = 'tool_orient_command_parser'

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self._name

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
        if len(tokens) < 2:
            raise ScaraSyntaxError(
                f'Invalid TOOL_ORIENT syntax at line {line_num}. '
                'Expected: TOOL_ORIENT <TANGENTIAL|FIXED|JOINT_LOCKED>'
            )

        mode: str = tokens[1].value.upper()

        if mode not in (
            ToolOrientMode.TANGENTIAL,
            ToolOrientMode.FIXED,
            ToolOrientMode.JOINT_LOCKED,
        ):
            raise ScaraSyntaxError(
                f'Invalid tool orientation mode {mode!r} at line {line_num}. '
                'Expected TANGENTIAL, FIXED, or JOINT_LOCKED'
            )

        sub_params: dict[str, object] = ParameterExtractor.extract_key_values(
            tokens=tokens[2:]
        )
        params: dict[str, object] = {InstructionParam.MODE: mode,}

        if InstructionParam.PHI in sub_params:
            phi_val: object = sub_params[InstructionParam.PHI]
            params[InstructionParam.PHI] = phi_val

        return ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
