# -*- coding: UTF-8 -*-

'''
Module
    export_command_executor_test.py
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
    Unit tests for ExportCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from tempfile import NamedTemporaryFile
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.infrastructure.command.export.export_command_definition import ExportCommandDefinition
from scaralang.infrastructure.command.export.export_command_executor import ExportCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExportCommandExecutor(TestCase):
    '''
        Test cases verifying ExportCommandExecutor.

        It defines:

            :methods:
                | test_execute_missing_script - Verifies handling when script file is absent.
                | test_execute_success_stdout - Verifies successful execution returning stdout.
                | test_execute_success_file_output - Verifies successful output file writing.
                | test_get_definition - Verifies definition getter.
    '''

    def setUp(self) -> None:
        '''Sets up test mocks and executor.'''
        self.cmd_def = ExportCommandDefinition()
        self.mock_dispatcher = MagicMock()
        self.executor = ExportCommandExecutor(
            definition=self.cmd_def,
            dispatcher=self.mock_dispatcher,
        )
        self.mock_service = MagicMock()

    def test_execute_missing_script(self) -> None:
        '''Verifies error returned when input script does not exist.'''
        res = self.executor.execute(
            params={'script': '/nonexistent/path/script.scara'},
            service=self.mock_service,
        )
        self.assertEqual(res['returncode'], 1)
        self.assertIn('script file does not exist', str(res['stderr']))

    def test_execute_success_stdout(self) -> None:
        '''Verifies export output emitted to stdout.'''
        with NamedTemporaryFile('w', delete=False, suffix='.scara') as tmp:
            tmp.write('HOME\nMOVE_J X=100.0 Y=50.0 Z=0.0\n')
            tmp_path = tmp.name

        try:
            self.mock_dispatcher.export.return_value = 'G00 X100.000 Y50.000 Z0.000'
            res = self.executor.execute(
                params={'script': tmp_path, 'format': 'gcode'},
                service=self.mock_service,
            )
            self.assertEqual(res['returncode'], 0)
            self.assertEqual(res['stdout'], 'G00 X100.000 Y50.000 Z0.000')
            self.mock_dispatcher.export.assert_called_once()
        finally:
            remove(tmp_path)

    def test_execute_success_file_output(self) -> None:
        '''Verifies export output written to destination file.'''
        with NamedTemporaryFile('w', delete=False, suffix='.scara') as tmp_in:
            tmp_in.write('HOME\n')
            tmp_in_path = tmp_in.name

        with NamedTemporaryFile('w', delete=False, suffix='.gcode') as tmp_out:
            tmp_out_path = tmp_out.name

        try:
            self.mock_dispatcher.export.return_value = 'G21\nG90\n'
            res = self.executor.execute(
                params={
                    'script': tmp_in_path,
                    'format': 'gcode',
                    'output': tmp_out_path,
                },
                service=self.mock_service,
            )
            self.assertEqual(res['returncode'], 0)
            self.assertIn('written to', str(res['stdout']))
            with open(tmp_out_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertEqual(content, 'G21\nG90\n')
        finally:
            remove(tmp_in_path)
            remove(tmp_out_path)

    def test_get_definition(self) -> None:
        '''Verifies get_definition returns the injected definition.'''
        self.assertEqual(self.executor.get_definition(), self.cmd_def)


if __name__ == '__main__':
    main()
