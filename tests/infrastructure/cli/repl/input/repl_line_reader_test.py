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
from unittest.mock import patch

from scaralang.infrastructure.cli.repl.input.irepl_line_reader import IReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader import ReplLineReader
from scaralang.infrastructure.cli.repl.input.repl_line_reader_factory import ReplLineReaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplLineReader(TestCase):
    '''
        Test cases verifying ReplLineReader and factory.

        It defines:

            :methods:
                | test_read_line - Verifies reading lines via standard input.
                | test_eof_handling - Verifies None returned when EOFError is raised.
                | test_keyboard_interrupt_handling - Verifies None returned on KeyboardInterrupt.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    @patch('builtins.input', return_value='  MOVE LINE X=100  \n')
    def test_read_line(self, _mock_input: object) -> None:
        '''Verifies reading lines via standard input.'''
        reader = ReplLineReader()
        line = reader.read_line()
        self.assertEqual(line, 'MOVE LINE X=100')

    @patch('builtins.input', side_effect=EOFError)
    def test_eof_handling(self, _mock_input: object) -> None:
        '''Verifies None is returned when EOFError is raised.'''
        reader = ReplLineReader()
        self.assertIsNone(reader.read_line())

    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_keyboard_interrupt_handling(self, _mock_input: object) -> None:
        '''Verifies None is returned when KeyboardInterrupt is raised.'''
        reader = ReplLineReader()
        self.assertIsNone(reader.read_line())

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory creation and runtime protocol check.'''
        reader = ReplLineReaderFactory.create_default()
        self.assertTrue(isinstance(reader, IReplLineReader))
        created_reader = ReplLineReaderFactory.create()
        self.assertTrue(isinstance(created_reader, IReplLineReader))
        self.assertEqual(ReplLineReaderFactory.get_version(), '1.0.4')
        self.assertEqual(reader.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
