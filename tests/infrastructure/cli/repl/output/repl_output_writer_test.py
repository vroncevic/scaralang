# -*- coding: UTF-8 -*-

'''
Module
    repl_output_writer_test.py
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
    Unit tests for ReplOutputWriter and factory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock
from unittest.mock import patch

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


class TestReplOutputWriter(TestCase):
    '''
        Test cases verifying ReplOutputWriter and factory.

        It defines:

            :methods:
                | test_write - Verifies emitting text via sys.stdout stream.
                | test_get_version - Verifies component version string.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    @patch('scaralang.infrastructure.cli.repl.output.repl_output_writer.stdout')
    def test_write(self, mock_stdout: MagicMock) -> None:
        '''Verifies emitting text via sys.stdout stream.'''
        writer = ReplOutputWriter()
        writer.write('Test output message')
        mock_stdout.write.assert_called_once_with('Test output message\n')
        mock_stdout.flush.assert_called_once()

    def test_get_version(self) -> None:
        '''Verifies component version string.'''
        writer = ReplOutputWriter()
        self.assertEqual(writer.get_version(), '1.0.4')

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory creation and runtime protocol check.'''
        writer = ReplOutputWriterFactory.create_default()
        self.assertTrue(isinstance(writer, IReplOutputWriter))
        created_writer = ReplOutputWriterFactory.create()
        self.assertTrue(isinstance(created_writer, IReplOutputWriter))
        self.assertEqual(ReplOutputWriterFactory.get_version(), '1.0.4')
        self.assertEqual(writer.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
