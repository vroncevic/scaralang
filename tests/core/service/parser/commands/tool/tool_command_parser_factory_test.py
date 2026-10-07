# -*- coding: UTF-8 -*-

'''
Module
    tool_command_parser_factory_test.py
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
    Unit tests for ToolCommandParserFactory service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.tool.tool_command_parser_factory import ToolCommandParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandParserFactoryTest(TestCase):
    '''
        Tests for ToolCommandParserFactory handler instantiation.
    '''

    def test_create_handlers(self) -> None:
        '''Verifies all 3 tool command parsers are instantiated.'''
        handlers = ToolCommandParserFactory.create_handlers()
        self.assertEqual(len(handlers), 3)
        for handler in handlers:
            self.assertIsInstance(handler, ICommandParser)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(ToolCommandParserFactory.get_version(), '1.0.7')
