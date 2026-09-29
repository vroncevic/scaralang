# -*- coding: UTF-8 -*-

'''
Module
    scara_script_validator_test.py
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
    Unit tests for ScaraScriptValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.dsl.validation.scara_script_validator import ScaraScriptValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraScriptValidator(TestCase):
    '''
        Test cases verifying ScaraScriptValidator operations.

        It defines:

            :methods:
                | test_validate_script_success - Verifies validation pass with valid script.
                | test_validate_script_lint_error - Verifies validation failure on lint errors.
                | test_validate_script_syntax_error - Verifies validation failure on parser error.
                | test_lint_script_success - Verifies linting returns diagnostics.
                | test_lint_script_syntax_error - Verifies linting catches syntax exception.
    '''

    def test_validate_script_success(self) -> None:
        '''
            Verifies validate_script passes when parser, linter, and compiler succeed.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        mock_parser.parse.return_value = program
        mock_linter.lint.return_value = ()
        mock_plan = MagicMock()
        mock_plan.count = 5
        mock_compiler.compile.return_value = mock_plan

        validator = ScaraScriptValidator(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        is_valid, messages = validator.validate_script(source='MOVE X10 Y20 Z0')
        self.assertTrue(is_valid)
        self.assertTrue(any('Validation PASSED' in m for m in messages))

    def test_validate_script_lint_error(self) -> None:
        '''
            Verifies validate_script fails when linter returns ERROR diagnostics.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        mock_parser.parse.return_value = program
        diag = ScaraDiagnostic(
            code='ERR_MOTION',
            severity=ScaraDiagnosticSeverity.ERROR,
            message='Kinematic limit exceeded',
            line=1,
            command='MOVE',
        )
        mock_linter.lint.return_value = (diag,)

        validator = ScaraScriptValidator(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        is_valid, messages = validator.validate_script(source='MOVE X999 Y999 Z0')
        self.assertFalse(is_valid)
        self.assertTrue(any('Kinematic limit exceeded' in m for m in messages))

    def test_validate_script_syntax_error(self) -> None:
        '''
            Verifies validate_script fails when parser raises ValueError.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ValueError('Invalid token')

        validator = ScaraScriptValidator(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        is_valid, messages = validator.validate_script(source='INVALID SCRIPT')
        self.assertFalse(is_valid)
        self.assertTrue(any('Validation failed: Invalid token' in m for m in messages))

    def test_lint_script_success(self) -> None:
        '''
            Verifies lint_script returns diagnostics from injected linter.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        mock_parser.parse.return_value = program
        diag = ScaraDiagnostic(
            code='WARN_SPEED',
            severity=ScaraDiagnosticSeverity.WARNING,
            message='High speed',
            line=1,
            command='MOVE',
        )
        mock_linter.lint.return_value = (diag,)

        validator = ScaraScriptValidator(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        diagnostics = validator.lint_script(source='MOVE X10 Y20 Z0 F180')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'WARN_SPEED')

    def test_lint_script_syntax_error(self) -> None:
        '''
            Verifies lint_script returns synthetic diagnostic when parser raises exception.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = TypeError('Malformed AST')

        validator = ScaraScriptValidator(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        diagnostics = validator.lint_script(source='BAD SCRIPT')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SYNTAX_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)


if __name__ == '__main__':
    main()
