# -*- coding: UTF-8 -*-

'''
Module
    cli_test.py
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
    Unit tests for scaralang CLI commands, executors, bundle factory and engine.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from pathlib import Path
from sys import path
from tempfile import NamedTemporaryFile
from unittest import TestCase

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scaralang.engine import Scaralang
from scaralang.setup.bundle import ScaralangBundle
from scaralang.setup.factory import ScaralangBundleFactory
from scaralang.setup.options import ScaralangBundleOptions
from scaralang.setup.opt_validator import ScaralangBundleOptionsValidator
from scaralang.setup.validator import ScaralangBundleValidator
from scaralang.infrastructure.command.compile_command_definition import CompileCommandDefinition
from scaralang.infrastructure.command.compile_command_executor import CompileCommandExecutor
from scaralang.infrastructure.command.disassemble_command_definition import DisassembleCommandDefinition
from scaralang.infrastructure.command.disassemble_command_executor import DisassembleCommandExecutor
from scaralang.infrastructure.command.info_command_definition import InfoCommandDefinition
from scaralang.infrastructure.command.info_command_executor import InfoCommandExecutor
from scaralang.infrastructure.command.lint_command_definition import LintCommandDefinition
from scaralang.infrastructure.command.lint_command_executor import LintCommandExecutor
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangCli(TestCase):
    '''
        Test cases verifying scaralang CLI commands and engine workflow.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and temporary files.
                | tearDown - Cleans up temporary resources.
                | test_bundle_factory - Verifies bundle creation.
                | test_info_command - Verifies info command output.
                | test_lint_command_clean - Verifies lint on clean script.
                | test_lint_command_error - Verifies lint with syntax errors.
                | test_compile_and_disassemble - Verifies end-to-end compilation and disassembly.
    '''

    def setUp(self) -> None:
        '''Sets up test fixtures.'''
        self._service = ScaraDslServiceFactory.create_default()
        self._temp_files: list[str] = []

    def tearDown(self) -> None:
        '''Cleans up temporary test files.'''
        for file_path in self._temp_files:
            if exists(file_path):
                remove(file_path)

    def _create_temp_file(self, content: str) -> str:
        '''Creates a temporary file with given content.'''
        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_name = f.name
        self._temp_files.append(temp_name)
        return temp_name

    def test_bundle_factory(self) -> None:
        '''Verifies bundle factory creates an initialized bundle.'''
        bundle = ScaralangBundleFactory.create_bundle()
        self.assertIsInstance(bundle, ScaralangBundle)
        self.assertTrue(ScaralangBundleValidator.is_valid(bundle))

        engine = Scaralang(bundle=bundle)
        self.assertTrue(engine.is_initialized())

    def test_info_command(self) -> None:
        '''Verifies info command execution.'''
        definition = InfoCommandDefinition()
        executor = InfoCommandExecutor(definition=definition)
        result = executor.execute(params={}, service=self._service)
        self.assertEqual(result.get('returncode'), 0)
        stdout_text = str(result.get('stdout', ''))
        self.assertIn('scaralang: SCARA Robotics Domain-Specific Language', stdout_text)
        self.assertIn('CRC-16-CCITT', stdout_text)

    def test_lint_command_clean(self) -> None:
        '''Verifies lint command on valid script.'''
        script_path = self._create_temp_file('HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        definition = LintCommandDefinition()
        executor = LintCommandExecutor(definition=definition)
        result = executor.execute(params={'script': script_path}, service=self._service)
        self.assertEqual(result.get('returncode'), 0)
        self.assertIn('No issues found', str(result.get('stdout', '')))

    def test_lint_command_error(self) -> None:
        '''Verifies lint command detects pneumatic conflict error.'''
        script_path = self._create_temp_file('HOME\nPUMP ON\nVALVE ON\n')
        definition = LintCommandDefinition()
        executor = LintCommandExecutor(definition=definition)
        result = executor.execute(params={'script': script_path}, service=self._service)
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('ERROR', str(result.get('stdout', '')))

    def test_compile_and_disassemble(self) -> None:
        '''Verifies end-to-end compile to binary file and disassembly.'''
        script_path = self._create_temp_file('HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        bin_path = script_path + '.bin'
        self._temp_files.append(bin_path)

        compile_def = CompileCommandDefinition()
        compile_exec = CompileCommandExecutor(definition=compile_def)
        compile_res = compile_exec.execute(
            params={'script': script_path, 'output': bin_path},
            service=self._service
        )
        self.assertEqual(compile_res.get('returncode'), 0)
        self.assertTrue(exists(bin_path))

        disasm_def = DisassembleCommandDefinition()
        disasm_exec = DisassembleCommandExecutor(definition=disasm_def)
        disasm_res = disasm_exec.execute(params={'file': bin_path}, service=self._service)
        self.assertEqual(disasm_res.get('returncode'), 0)
        disasm_out = str(disasm_res.get('stdout', ''))
        self.assertIn('CMD_HOME', disasm_out)
        self.assertIn('CMD_MOVE_JOINT_STEPS', disasm_out)
        self.assertIn('PUMP ON', disasm_out)
