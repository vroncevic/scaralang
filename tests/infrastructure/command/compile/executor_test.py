# -*- coding: UTF-8 -*-

'''
Module
    executor_test.py
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
    Unit tests for CompileCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile.executor_factory import CompileCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileCommandExecutor(TestCase):
    '''
        Test cases verifying CompileCommandExecutor.

        It defines:

            :methods:
                | setUp - Initializes fixtures.
                | tearDown - Cleans up temporary resources.
                | write_test_script - Writes content to temporary file.
                | test_compile_missing_file - Verifies handling of missing script.
                | test_compile_to_file - Verifies compiling to binary output file.
                | test_compile_verbose - Verifies compiling with verbose output telemetry.
                | test_compile_hex - Verifies compiling with hex output flag.
                | test_compile_dump_frames - Verifies compiling with dump_frames inspection flag.
                | test_compile_default_message - Verifies compiling with default status message.
                | test_compile_error_exception - Verifies error handling when write fails.
                | test_compile_syntax_error - Verifies handling of syntax error during compile.
                | test_compile_semantic_error - Verifies handling of semantic error during compile.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.cmd_def = CompileCommandDefinition()
        self.executor = CompileCommandExecutorFactory.create_default()
        self.temp_files: list[str] = []

    def tearDown(self) -> None:
        '''
            Cleans up temporary resources.
        '''
        for path in self.temp_files:
            if exists(path):
                remove(path)

    def write_test_script(self, *, text: str) -> str:
        '''
            Writes content to a temporary script file.
        '''
        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as f:
            f.write(text)
            temp_name = f.name
        self.temp_files.append(temp_name)
        return temp_name

    def test_compile_missing_file(self) -> None:
        '''
            Verifies handling of non-existent input script.
        '''
        res = self.executor.execute(
            params={'script': '/nonexistent/file.scara'},
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('does not exist', str(res.get('stderr', '')))

    def test_compile_to_file(self) -> None:
        '''
            Verifies compiling to destination binary file.
        '''
        script_path = self.write_test_script(text='HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        bin_path = script_path + '.bin'
        self.temp_files.append(bin_path)

        res = self.executor.execute(
            params={'script': script_path, 'output': bin_path},
        )
        self.assertEqual(res.get('returncode'), 0)
        self.assertTrue(exists(bin_path))

    def test_compile_verbose(self) -> None:
        '''
            Verifies compile command with verbose telemetry enabled.
        '''
        script_path = self.write_test_script(text='HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\n')
        res = self.executor.execute(
            params={'script': script_path, 'verbose': True},
        )
        self.assertEqual(res.get('returncode'), 0)
        stdout_text = str(res.get('stdout', ''))
        self.assertIn('Compilation Telemetry:', stdout_text)
        self.assertIn('Source Instructions:', stdout_text)
        self.assertIn('Estimated Duration:', stdout_text)

    def test_compile_hex(self) -> None:
        '''
            Verifies compile command with hex output flag.
        '''
        script_path = self.write_test_script(text='HOME\n')
        res = self.executor.execute(
            params={'script': script_path, 'hex': True},
        )
        self.assertEqual(res.get('returncode'), 0)
        self.assertTrue(len(str(res.get('stdout', ''))) > 0)

    def test_compile_dump_frames(self) -> None:
        '''
            Verifies compile command with dump_frames inspection flag.
        '''
        script_path = self.write_test_script(text='HOME\n')
        res = self.executor.execute(
            params={'script': script_path, 'dump_frames': True},
        )
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('SCARA BINARY FRAME INSPECTION', str(res.get('stdout', '')))

    def test_compile_default_message(self) -> None:
        '''
            Verifies compile command with default status output.
        '''
        script_path = self.write_test_script(text='HOME\n')
        res = self.executor.execute(
            params={'script': script_path},
        )
        self.assertEqual(res.get('returncode'), 0)
        self.assertIn('Successfully compiled', str(res.get('stdout', '')))

    def test_compile_error_exception(self) -> None:
        '''
            Verifies handling of unexpected error during compilation output write.
        '''
        script_path = self.write_test_script(text='HOME\n')
        res = self.executor.execute(
            params={'script': script_path, 'output': '/nonexistent_dir/out.bin'},
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('compile error', str(res.get('stderr', '')))

    def test_compile_syntax_error(self) -> None:
        '''
            Verifies handling and structured formatting of syntax error.
        '''
        script_path = self.write_test_script(text='UNKNOWN_COMMAND\n')
        res = self.executor.execute(
            params={'script': script_path},
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('[SYNTAX]', str(res.get('stderr', '')))

    def test_compile_semantic_error(self) -> None:
        '''
            Verifies handling and structured formatting of semantic error.
        '''
        script_path = self.write_test_script(text='MOVE_PALLET P1 INDEX=1\n')
        res = self.executor.execute(
            params={'script': script_path},
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('[SEMANTIC]', str(res.get('stderr', '')))

    def test_get_definition(self) -> None:
        '''
            Verifies definition getter.
        '''
        self.assertEqual(self.executor.get_definition().name, self.cmd_def.name)


if __name__ == '__main__':
    main()
