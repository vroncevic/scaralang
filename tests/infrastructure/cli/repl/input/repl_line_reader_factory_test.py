# -*- coding: UTF-8 -*-

'''
Module
    repl_line_reader_factory_test.py
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
    Unit tests for ReplLineReaderFactory class.
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
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplLineReaderFactory(TestCase):
    '''
        Test cases verifying ReplLineReaderFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns default ReplLineReader.
                | test_create - Verifies factory builds ReplLineReader instance.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns default ReplLineReader instance.'''
        reader = ReplLineReaderFactory.create_default()
        self.assertIsInstance(reader, ReplLineReader)
        self.assertIsInstance(reader, IReplLineReader)

    def test_create(self) -> None:
        '''Verifies factory builds ReplLineReader instance.'''
        reader = ReplLineReaderFactory.create()
        self.assertIsInstance(reader, ReplLineReader)
        self.assertIsInstance(reader, IReplLineReader)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            ReplLineReaderFactory.get_version(), '1.0.5'
        )


if __name__ == '__main__':
    main()
