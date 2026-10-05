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
    Unit tests for LintCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.infrastructure.command.lint.definition import LintCommandDefinition
from scaralang.infrastructure.command.lint.error.lint_error_handler_factory import LintErrorHandlerFactory
from scaralang.infrastructure.command.lint.executor import LintCommandExecutor
from scaralang.infrastructure.command.lint.executor_factory import LintCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
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
                | create_test_file - Creates temporary file helper.
                | test_lint_missing_file - Verifies handling of non-existent script.
                | test_lint_clean_script - Verifies clean lint execution on valid script.
                | test_lint_error_script - Verifies diagnostic errors on conflicting script.
                | test_lint_error_handling - Verifies handling of lint exceptions.
                | test_lint_domain_error_handling - Verifies handling of domain exception.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.cmd_def = LintCommandDefinition()
        self.executor = LintCommandExecutorFactory.create_default()
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
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('does not exist', str(res.get('stderr', '')))

    def test_lint_clean_script(self) -> None:
        '''
            Verifies lint command on valid script.
        '''
        path = self.create_test_file('HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        result = self.executor.execute(params={'script': path})
        self.assertEqual(result.get('returncode'), 0)
        self.assertIn('No issues found', str(result.get('stdout', '')))

    def test_lint_error_script(self) -> None:
        '''
            Verifies lint command detects pneumatic conflict error.
        '''
        path = self.create_test_file('HOME\nPUMP ON\nVALVE ON\n')
        result = self.executor.execute(params={'script': path})
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('ERROR', str(result.get('stdout', '')))

    def test_get_definition(self) -> None:
        '''
            Verifies definition getter.
        '''
        self.assertEqual(self.executor.get_definition().name, self.cmd_def.name)

    def test_lint_error_handling(self) -> None:
        '''
            Verifies handling when lint service raises an exception.
        '''
        mock_service = MagicMock()
        mock_service.lint_script.side_effect = ValueError('Failed to parse')
        executor = LintCommandExecutor(
            definition=self.cmd_def,
            service=mock_service,
            diagnostic_formatter=MagicMock(),
            error_handler=LintErrorHandlerFactory.create(),
        )
        path = self.create_test_file('HOME\n')
        result = executor.execute(params={'script': path})
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('lint error: Failed to parse', str(result.get('stderr', '')))

    def test_lint_domain_error_handling(self) -> None:
        '''
            Verifies handling and structured formatting of domain ScaraSyntaxError.
        '''
        mock_service = MagicMock()
        mock_service.lint_script.side_effect = ScaraSyntaxError('invalid keyword')
        executor = LintCommandExecutor(
            definition=self.cmd_def,
            service=mock_service,
            diagnostic_formatter=MagicMock(),
            error_handler=LintErrorHandlerFactory.create(),
        )
        path = self.create_test_file('HOME\n')
        result = executor.execute(params={'script': path})
        self.assertEqual(result.get('returncode'), 1)
        self.assertIn('lint error: [SYNTAX] invalid keyword', str(result.get('stderr', '')))


if __name__ == '__main__':
    main()
