# -*- coding: UTF-8 -*-

'''
Module
    frame_command_parser.py
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
    Implementation of ICommandParser parsing FRAME_SET and FRAME_RESET commands.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import CommandType
from scaralang.core.model.dsl.ast.instruction import Instruction
from scaralang.core.model.dsl.token.token import Token
from scaralang.core.service.dsl.ast.iinstruction_factory import IInstructionFactory
from scaralang.core.service.dsl.ast.instruction_factory import InstructionFactory
from scaralang.core.service.dsl.parser.parameter_extractor import ParameterExtractor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameCommandParser:
    '''
        Command parser handler for work frame definition and reset instructions.

        It defines:

            :attributes:
                | _instruction_factory - Injected IInstructionFactory instance.
            :methods:
                | __init__ - Initializes FrameCommandParser with injected factory.
                | can_parse - Checks whether command is FRAME_SET or FRAME_RESET.
                | parse - Parses frame statement tokens into Instruction.
    '''

    _instruction_factory: IInstructionFactory

    def __init__(self, *, instruction_factory: IInstructionFactory = InstructionFactory()) -> None:
        '''
            Initializes FrameCommandParser constructor.

            :param instruction_factory: Injected IInstructionFactory instance.
        '''
        self._instruction_factory = instruction_factory

    def can_parse(self, *, command_name: str) -> bool:
        '''
            Checks if command is FRAME_SET or FRAME_RESET.

            :param command_name: Command keyword string.
            :return: True if match, False otherwise.
        '''
        return command_name in (
            'FRAME_SET', 'FRAME_RESET', 'SET_FRAME', 'RESET_FRAME'
        )

    def parse(
        self,
        *,
        tokens: tuple[Token, ...],
        line_num: int,
        raw_text: str,
    ) -> Instruction:
        '''
            Parses frame statement into Instruction.

            :param tokens: Statement token tuple.
            :param line_num: Line number in source code.
            :param raw_text: Original statement text.
            :return: Instruction node.
        '''
        cmd = tokens[0].value.upper()

        if cmd in ('FRAME_RESET', 'RESET_FRAME'):
            return self._instruction_factory.create(
                command_type=CommandType.FRAME_RESET,
                line_number=line_num,
                raw_text=raw_text,
                parameters={},
            )

        params = ParameterExtractor.extract_key_values(tokens=tokens[1:])

        return self._instruction_factory.create(
            command_type=CommandType.FRAME_SET,
            line_number=line_num,
            raw_text=raw_text,
            parameters=params,
        )
