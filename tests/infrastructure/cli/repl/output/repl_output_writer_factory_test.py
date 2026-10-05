# -*- coding: UTF-8 -*-

'''
Module
    repl_output_writer_factory_test.py
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
    Unit tests for ReplOutputWriterFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.cli.repl.output.irepl_output_writer import IReplOutputWriter
from scaralang.infrastructure.cli.repl.output.repl_output_writer import ReplOutputWriter
from scaralang.infrastructure.cli.repl.output.repl_output_writer_factory import ReplOutputWriterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplOutputWriterFactory(TestCase):
    '''
        Test cases verifying ReplOutputWriterFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns default ReplOutputWriter.
                | test_create - Verifies factory builds ReplOutputWriter instance.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns default ReplOutputWriter instance.'''
        writer = ReplOutputWriterFactory.create_default()
        self.assertIsInstance(writer, ReplOutputWriter)
        self.assertIsInstance(writer, IReplOutputWriter)

    def test_create(self) -> None:
        '''Verifies factory builds ReplOutputWriter instance.'''
        writer = ReplOutputWriterFactory.create()
        self.assertIsInstance(writer, ReplOutputWriter)
        self.assertIsInstance(writer, IReplOutputWriter)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            ReplOutputWriterFactory.get_version(), '1.0.4'
        )


if __name__ == '__main__':
    main()
