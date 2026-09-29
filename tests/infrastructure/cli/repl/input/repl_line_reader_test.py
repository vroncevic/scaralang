# -*- coding: UTF-8 -*-

'''
Module
    repl_line_reader_test.py
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
    Unit tests for ReplLineReader and ReplLineReaderFactory classes.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.input.irepl_line_reader import IReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader import ReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplLineReader(TestCase):
    '''
        Test cases verifying ReplLineReader and factory.

        It defines:

            :methods:
                | test_custom_reader_func - Verifies reading lines via custom callable.
                | test_eof_handling - Verifies None returned when EOFError is raised.
                | test_keyboard_interrupt_handling - Verifies None returned on KeyboardInterrupt.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    def test_custom_reader_func(self) -> None:
        '''Verifies reading lines via injected callable.'''
        reader = ReplLineReader(reader_func=lambda prompt: '  MOVE LINE X=100  \n')
        line = reader.read_line()
        self.assertEqual(line, 'MOVE LINE X=100')

    def test_eof_handling(self) -> None:
        '''Verifies None is returned when EOFError is raised.'''
        def raise_eof(_: str) -> str:
            raise EOFError()

        reader = ReplLineReader(reader_func=raise_eof)
        self.assertIsNone(reader.read_line())

    def test_keyboard_interrupt_handling(self) -> None:
        '''Verifies None is returned when KeyboardInterrupt is raised.'''
        def raise_interrupt(_: str) -> str:
            raise KeyboardInterrupt()

        reader = ReplLineReader(reader_func=raise_interrupt)
        self.assertIsNone(reader.read_line())

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory creation and runtime protocol check.'''
        reader = ReplLineReaderFactory.create_default()
        self.assertTrue(isinstance(reader, IReplLineReader))
        custom_reader = ReplLineReaderFactory.create(
            reader_func=lambda prompt: 'test'
        )
        self.assertTrue(isinstance(custom_reader, IReplLineReader))
        self.assertEqual(ReplLineReaderFactory.get_version(), '1.0.0')


if __name__ == '__main__':
    main()
