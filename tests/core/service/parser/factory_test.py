# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ParserFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.dependencies import ParserDependencies
from scaralang.core.service.parser.factory import ParserFactory
from scaralang.core.service.parser.iparser import IScaraParser
from scaralang.core.service.parser.lexer.factory import LexerFactory
from scaralang.core.service.parser.provides import ParserProvides
from scaralang.core.service.parser.splitter.factory import SplitterFactory
from scaralang.infrastructure.parser.instruction.factory import DefaultInstructionParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestParserFactory(TestCase):
    '''
        Test cases verifying ParserFactory instance creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns ParserProvides with IScaraParser.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies that factory returns a ParserProvides instance.
        '''
        deps = ParserDependencies(
            lexer=LexerFactory.create().lexer,
            line_splitter=SplitterFactory.create().splitter,
            line_parser=DefaultInstructionParserFactory.create().parser,
        )
        provides = ParserFactory.create(dependencies=deps)
        self.assertIsInstance(provides, ParserProvides)
        self.assertIsInstance(provides.parser, IScaraParser)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns a valid version string.
        '''
        version = ParserFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
