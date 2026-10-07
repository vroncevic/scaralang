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
    Unit tests for DecompileCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.exceptions.scara_protocol_error import ScaraProtocolError
from scaralang.infrastructure.command.compile.executor_factory import CompileCommandExecutorFactory
from scaralang.infrastructure.command.decompile.definition import DecompileCommandDefinition
from scaralang.infrastructure.command.decompile.error.decompile_error_handler_factory import DecompileErrorHandlerFactory
from scaralang.infrastructure.command.decompile.executor import DecompileCommandExecutor
from scaralang.infrastructure.command.decompile.executor_factory import DecompileCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDecompileCommandExecutor(TestCase):
    '''
        Test cases verifying DecompileCommandExecutor.

        It defines:

            :methods:
                | setUp - Initializes fixtures.
                | tearDown - Cleans up temporary resources.
                | create_source_file - Creates temporary source file helper.
                | test_decompile_missing_file - Verifies handling of absent file.
                | test_decompile_to_stdout - Verifies decompile to stdout.
                | test_decompile_to_output_file - Verifies decompile to output file.
                | test_decompile_output_error - Verifies handling of write output error.
                | test_decompile_domain_error - Verifies handling of domain exception.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.cmd_def = DecompileCommandDefinition()
        self.executor = DecompileCommandExecutorFactory.create_default()
        self.temp_files: list[str] = []

    def tearDown(self) -> None:
        '''
            Cleans up temporary resources.
        '''
        for path in self.temp_files:
            if exists(path):
                remove(path)

    def create_source_file(self, content: str) -> str:
        '''
            Creates temporary source file helper.
        '''
        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_name = f.name
        self.temp_files.append(temp_name)
        return temp_name

    def test_decompile_missing_file(self) -> None:
        '''
            Verifies handling of non-existent input binary file.
        '''
        res = self.executor.execute(
            params={'file': '/nonexistent/file.bin'},
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('does not exist', str(res.get('stderr', '')))

    def test_decompile_to_stdout(self) -> None:
        '''
            Verifies compiling script to binary and decompiling to stdout.
        '''
        script_path = self.create_source_file('HOME\nPUMP ON\n')
        bin_path = script_path + '.bin'
        self.temp_files.append(bin_path)

        compile_exec = CompileCommandExecutorFactory.create_default()
        compile_exec.execute(
            params={'script': script_path, 'output': bin_path},
        )

        res = self.executor.execute(params={'file': bin_path})
        self.assertEqual(res.get('returncode'), 0)
        decompiled_out = str(res.get('stdout', ''))
        self.assertIn('HOME', decompiled_out)
        self.assertIn('PUMP ON', decompiled_out)

    def test_decompile_to_output_file(self) -> None:
        '''
            Verifies decompiling binary file directly to an output file.
        '''
        script_path = self.create_source_file('HOME\nVALVE ON\n')
        bin_path = script_path + '.bin'
        out_script_path = script_path + '.decompiled.scara'
        self.temp_files.append(bin_path)
        self.temp_files.append(out_script_path)

        compile_exec = CompileCommandExecutorFactory.create_default()
        compile_exec.execute(
            params={'script': script_path, 'output': bin_path},
        )

        res = self.executor.execute(
            params={'file': bin_path, 'output': out_script_path},
        )
        self.assertEqual(res.get('returncode'), 0)
        self.assertTrue(exists(out_script_path))
        with open(out_script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('HOME', content)
        self.assertIn('VALVE ON', content)

    def test_get_definition(self) -> None:
        '''
            Verifies definition retrieval.
        '''
        self.assertEqual(self.executor.get_definition().name, 'decompile')

    def test_decompile_output_error(self) -> None:
        '''
            Verifies error handling when writing decompiled output fails.
        '''
        with NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            f.write(b'')
            bin_name = f.name
        self.temp_files.append(bin_name)
        res = self.executor.execute(
            params={'file': bin_name, 'output': '/nonexistent_dir/file.scara'}
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('decompile error:', str(res.get('stderr', '')))

    def test_decompile_domain_error(self) -> None:
        '''
            Verifies handling and structured formatting of domain ScaraProtocolError.
        '''
        mock_service = MagicMock()
        mock_service.decompile.side_effect = ScaraProtocolError('corrupted frame')
        executor = DecompileCommandExecutor(
            definition=self.cmd_def,
            service=mock_service,
            error_handler=DecompileErrorHandlerFactory.create(),
        )
        with NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
            f.write(b'\x00\x01')
            bin_name = f.name
        self.temp_files.append(bin_name)
        res = executor.execute(params={'file': bin_name})
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('[PROTOCOL] corrupted frame', str(res.get('stderr', '')))


if __name__ == '__main__':
    main()
