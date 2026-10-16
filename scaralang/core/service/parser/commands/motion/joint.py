# -*- coding: UTF-8 -*-

'''
Module
    joint.py
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
    Implementation of command parser parsing fast point-to-point MOVE_J commands.
'''

from __future__ import annotations
from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.token.scara_token import ScaraToken
from scaralang.core.service.parser.commands.parameter.extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointParser:
    '''
        Command parser handler for MOVE_J joint motion instructions.

        It defines:

            :cvar NAME: Component identification name.
            :cvar PARAMS_START_INDEX: Start index of parameters in token sequence.
            :cvar PARSED_COMMAND: Target command keyword string.
            :methods:
                | name - Property returning component name.
                | can_parse - Checks whether command is MOVE_J.
                | parse - Parses MOVE_J statement tokens into ScaraInstruction.
    '''

    NAME: ClassVar[str] = 'joint_parser'
    PARAMS_START_INDEX: ClassVar[int] = 1
    PARSED_COMMAND: ClassVar[str] = ScaraCommandType.MOVE_J

    @property
    def name(self) -> str:
        '''
            Gets component identification name.

            :return: Component name string.
        '''
        return self.NAME

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is MOVE_J.

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
            Parses MOVE_J statement into ScaraInstruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: ScaraInstruction node.
        '''
        joint_params = ParameterExtractor.extract_key_values(
            tokens=tokens[self.PARAMS_START_INDEX:]
        )

        return ScaraInstruction(
            command_type=self.PARSED_COMMAND,
            line_number=line_num,
            raw_text=raw_text,
            parameters=joint_params,
        )
