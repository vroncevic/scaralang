# -*- coding: UTF-8 -*-

'''
Module
    icommand_parser_provider_test.py
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
    Unit tests for ICommandParserProvider structural protocol.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.service.parser.commands.config.config_command_parser_factory import ConfigCommandParserFactory
from scaralang.core.service.parser.commands.flow.flow_command_parser_factory import FlowCommandParserFactory
from scaralang.core.service.parser.commands.frame.frame_command_parser_factory import FrameCommandParserFactory
from scaralang.core.service.parser.commands.icommand_parser_provider import ICommandParserProvider
from scaralang.core.service.parser.commands.macro.macro_command_parser_factory import MacroCommandParserFactory
from scaralang.core.service.parser.commands.motion.motion_command_parser_factory import MotionCommandParserFactory
from scaralang.core.service.parser.commands.tool.tool_command_parser_factory import ToolCommandParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ICommandParserProviderTest(TestCase):
    '''
        Tests verifying structural protocol conformance for ICommandParserProvider.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies all 6 domain factories satisfy ICommandParserProvider.'''
        factories: tuple[type[object], ...] = (
            MotionCommandParserFactory,
            MacroCommandParserFactory,
            FrameCommandParserFactory,
            ConfigCommandParserFactory,
            FlowCommandParserFactory,
            ToolCommandParserFactory,
        )
        for factory in factories:
            self.assertTrue(
                isinstance(factory, ICommandParserProvider),
                f'{factory.__name__} does not satisfy ICommandParserProvider',
            )

    def test_invalid_provider_rejection(self) -> None:
        '''Verifies object lacking required protocol methods is rejected.'''
        class InvalidProvider:
            '''Dummy invalid provider lacking required protocol methods.'''

        self.assertFalse(isinstance(InvalidProvider, ICommandParserProvider))
