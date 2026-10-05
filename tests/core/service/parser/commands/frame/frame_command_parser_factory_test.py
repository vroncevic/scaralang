# -*- coding: UTF-8 -*-

'''
Module
    frame_command_parser_factory_test.py
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
    Unit tests for FrameCommandParserFactory service component.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.service.parser.commands.frame.frame_command_parser_factory import FrameCommandParserFactory
from scaralang.core.service.parser.commands.icommand_parser import ICommandParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameCommandParserFactoryTest(TestCase):
    '''
        Tests for FrameCommandParserFactory handler instantiation.
    '''

    def test_create_handlers(self) -> None:
        '''Verifies all 2 frame command parsers are instantiated.'''
        handlers = FrameCommandParserFactory.create_handlers()
        self.assertEqual(len(handlers), 2)
        for handler in handlers:
            self.assertIsInstance(handler, ICommandParser)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertEqual(FrameCommandParserFactory.get_version(), '1.0.5')
