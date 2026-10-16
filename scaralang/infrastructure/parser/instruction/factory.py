# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing default full-stack InstructionLineParser composition.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.service.parser.commands.config.factory import ConfigFactory
from scaralang.core.service.parser.commands.flow.factory import FlowFactory
from scaralang.core.service.parser.commands.frame.factory import FrameFactory
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.icommand_parser_provider import ICommandParserProvider
from scaralang.core.service.parser.commands.macro.factory import MacroFactory
from scaralang.core.service.parser.commands.motion.factory import MotionFactory
from scaralang.core.service.parser.commands.tool.factory import ToolFactory
from scaralang.core.service.parser.instruction.dependencies import InstructionDependencies
from scaralang.core.service.parser.instruction.factory import InstructionFactory
from scaralang.core.service.parser.instruction.provides import InstructionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultInstructionParserFactory:
    '''
        Factory providing default full-stack InstructionLineParser composition.

        It defines:

            :attributes:
                | _DEFAULT_DOMAINS - Tuple of domain provider factory classes.
            :methods:
                | create - Builds and returns default InstructionProvides instance.
                | get_version - Returns factory version string.
    '''

    _DEFAULT_DOMAINS: ClassVar[tuple[type[ICommandParserProvider], ...]] = (
        MotionFactory,
        MacroFactory,
        FrameFactory,
        ConfigFactory,
        FlowFactory,
        ToolFactory,
    )

    @classmethod
    def create(cls) -> InstructionProvides:
        '''
            Builds and returns default InstructionProvides instance.

            :return: Fully configured InstructionProvides instance.
            :exceptions: None.
        '''
        handlers: tuple[ICommandParser, ...] = tuple(
            handler
            for domain_factory in cls._DEFAULT_DOMAINS
            for handler in domain_factory.create().parsers
        )
        return InstructionFactory.create(
            dependencies=InstructionDependencies(handlers=handlers)
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
