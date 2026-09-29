# -*- coding: UTF-8 -*-

'''
Module
    lint_command_executor_test.py
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
    Unit tests for LintCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main

from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.core.service.linter.diagnostic.scara_diagnostic_formatter_factory import ScaraDiagnosticFormatterFactory
from scaralang.infrastructure.command.lint.lint_command_definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.lint_command_executor import LintCommandExecutor
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLintCommandExecutor(TestCase):
    '''
        Test cases verifying LintCommandExecutor.

        It defines:

            :methods:
                | setUp - Initializes fixtures.
                | tearDown - Cleans up temporary resources.
                | test_lint_missing_file - Verifies handling of non-existent script.
                | test_lint_clean_script - Verifies clean lint execution on valid script.
                | test_lint_error_script - Verifies diagnostic errors on conflicting script.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.cmd_def = LintCommandDefinition()
        self.formatter = ScaraDiagnosticFormatterFactory.create()
        self.executor = LintCommandExecutor(
            definition=self.cmd_def,
            diagnostic_formatter=self.formatter,
        )
        self.service = ScaraDslServiceFactory.create_default(
            frame_builder=BinaryFrameBuilderFactory.create(),
            frame_parser=BinaryFrameParserFactory.create_default(),
            payload_unpacker=BinaryPayloadUnpackerFactory.create(),
        )
        self.temp_files: list[str] = []

    def tearDown(self) -> None:
        '''
            Cleans up temporary files.
        '''
        for path in self.temp_files:
            if exists(path):
                remove(path)

    def create_test_file(self, content: str) -> str:
        '''
            Creates temporary file helper.
        '''
        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_name = f.name
        self.temp_files.append(temp_name)
        return temp_name

    def test_lint_missing_file(self) -> None:
        '''
            Verifies error returned when script file is missing.
        '''
        res = self.executor.execute(
            params={'script': '/nonexistent/file.scara'},
            service=self.service,
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('does not exist', str(res.get('stderr', '')))

    def test_lint_clean_script(self) -> None:
        '''
            Verifies lint command on valid script.
        '''
        path = self.create_test_file('HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        result = self.executor.execute(params={'script': path}, service=self.service)
        self.assertEqual(result.get('returncode'), 0)
        self.assertIn('No issues found', str(result.get('stdout', '')))

    def test_lint_error_script(self) -> None:
        '''
            Verifies lint command detects pneumatic conflict error.
        '''
        path = self.create_test_file('HOME\nPUMP ON\nVALVE ON\n')
        result = self.executor.execute(params={'script': path}, service=self.service)
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('ERROR', str(result.get('stdout', '')))

    def test_get_definition(self) -> None:
        '''
            Verifies definition getter.
        '''
        self.assertEqual(self.executor.get_definition(), self.cmd_def)


if __name__ == '__main__':
    main()
