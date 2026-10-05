# -*- coding: UTF-8 -*-

'''
Module
    instruction_line_parser_factory.py
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
    Factory instantiating and wiring IInstructionLineParser instances.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from scaralang.core.service.parser.commands.config.config_command_parser_factory import ConfigCommandParserFactory
from scaralang.core.service.parser.commands.flow.flow_command_parser_factory import FlowCommandParserFactory
from scaralang.core.service.parser.commands.frame.frame_command_parser_factory import FrameCommandParserFactory
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.icommand_parser_provider import ICommandParserProvider
from scaralang.core.service.parser.commands.macro.macro_command_parser_factory import MacroCommandParserFactory
from scaralang.core.service.parser.commands.motion.motion_command_parser_factory import MotionCommandParserFactory
from scaralang.core.service.parser.commands.tool.tool_command_parser_factory import ToolCommandParserFactory
from scaralang.core.service.parser.instruction.iinstruction_line_parser import IInstructionLineParser
from scaralang.core.service.parser.instruction.instruction_line_parser import InstructionLineParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionLineParserFactory:
    '''
        Factory providing wired IInstructionLineParser instances using domain providers.

        It defines:

            :attributes:
                | _DEFAULT_DOMAINS - Tuple of domain provider factory classes.
            :methods:
                | create - Builds and wires InstructionLineParser with domain provider handlers.
                | create_with_handlers - Builds InstructionLineParser with custom command handlers.
                | default_domains - Returns tuple of registered domain provider factory types.
                | get_version - Returns factory version string.
    '''

    _DEFAULT_DOMAINS: ClassVar[tuple[type[ICommandParserProvider], ...]] = (
        MotionCommandParserFactory,
        MacroCommandParserFactory,
        FrameCommandParserFactory,
        ConfigCommandParserFactory,
        FlowCommandParserFactory,
        ToolCommandParserFactory,
    )

    @classmethod
    def create(cls) -> IInstructionLineParser:
        '''
            Builds and wires InstructionLineParser with default domain command handlers.

            :return: IInstructionLineParser structural protocol instance.
            :exceptions: None.
        '''
        handlers = tuple(
            handler
            for domain_factory in cls._DEFAULT_DOMAINS
            for handler in domain_factory.create_handlers()
        )
        return cls.create_with_handlers(handlers=handlers)

    @classmethod
    def create_with_handlers(
        cls, *, handlers: Sequence[ICommandParser]
    ) -> IInstructionLineParser:
        '''
            Builds InstructionLineParser with custom command handlers.

            :param handlers: Explicit sequence of custom ICommandParser handlers.
            :return: IInstructionLineParser structural protocol instance.
            :exceptions: None.
        '''
        return InstructionLineParser(handlers=handlers)

    @classmethod
    def default_domains(cls) -> tuple[type[ICommandParserProvider], ...]:
        '''
            Returns tuple of registered default domain command parser providers.

            :return: Tuple of domain provider factory types.
        '''
        return cls._DEFAULT_DOMAINS

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Version string.
        '''
        return __version__
