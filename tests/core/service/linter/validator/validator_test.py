# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for ScriptValidator class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.severity import ScaraDiagnosticSeverity
from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.linter.validator.dependencies import ValidatorDependencies
from scaralang.core.service.linter.validator.validator import ScriptValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScriptValidator(TestCase):
    '''
        Test cases verifying ScriptValidator operations.

        It defines:

            :methods:
                | test_validate_script_success - Verifies validation pass with valid script.
                | test_validate_script_lint_error - Verifies validation failure on lint errors.
                | test_validate_script_syntax_error - Verifies validation failure on parser error.
                | test_validate_script_domain_syntax - Verifies failure on ScaraSyntaxError.
                | test_validate_script_domain_kinematics - Verifies failure on ScaraKinematicsError.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_validate_script_success(self) -> None:
        '''
            Verifies validate_script passes when parser, linter, and compiler succeed.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        mock_program = ScaraProgram(instructions=(MagicMock(),))
        mock_parser.parse.return_value = mock_program
        mock_linter.lint.return_value = ()
        mock_plan = MagicMock()
        mock_plan.count = 5
        mock_compiler.compile.return_value = mock_plan

        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=mock_parser,
                linter=mock_linter,
                compiler=mock_compiler,
            )
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

        mock_program = ScaraProgram(instructions=(MagicMock(),))
        mock_parser.parse.return_value = mock_program
        error_diag = ScaraDiagnostic(
            code='SCARA_E001',
            severity=ScaraDiagnosticSeverity.ERROR,
            message='Kinematic limit exceeded',
            line=2,
            command='MOVE',
        )
        mock_linter.lint.return_value = (error_diag,)

        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=mock_parser,
                linter=mock_linter,
                compiler=mock_compiler,
            )
        )
        is_valid, messages = validator.validate_script(source='MOVE X999 Y999 Z0')
        self.assertFalse(is_valid)
        self.assertTrue(any('Kinematic limit exceeded' in m for m in messages))
        mock_compiler.compile.assert_not_called()

    def test_validate_script_syntax_error(self) -> None:
        '''
            Verifies validate_script fails when parser raises ValueError.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ValueError('Syntax error: invalid token')

        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=mock_parser,
                linter=mock_linter,
                compiler=mock_compiler,
            )
        )
        is_valid, messages = validator.validate_script(source='INVALID SCRIPT')
        self.assertFalse(is_valid)
        self.assertTrue(any('Validation failed' in m for m in messages))

    def test_validate_script_domain_syntax(self) -> None:
        '''
            Verifies validate_script fails gracefully on ScaraSyntaxError.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ScaraSyntaxError('Syntax parse error')

        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=mock_parser,
                linter=mock_linter,
                compiler=mock_compiler,
            )
        )
        is_valid, messages = validator.validate_script(source='INVALID')
        self.assertFalse(is_valid)
        self.assertTrue(any('Validation failed' in m for m in messages))

    def test_validate_script_domain_kinematics(self) -> None:
        '''
            Verifies validate_script fails gracefully on ScaraKinematicsError.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        mock_program = ScaraProgram(instructions=(MagicMock(),))
        mock_parser.parse.return_value = mock_program
        mock_linter.lint.return_value = ()
        mock_compiler.compile.side_effect = ScaraKinematicsError(
            'Unreachable point'
        )

        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=mock_parser,
                linter=mock_linter,
                compiler=mock_compiler,
            )
        )
        is_valid, messages = validator.validate_script(source='MOVE X999 Y999 Z0')
        self.assertFalse(is_valid)
        self.assertTrue(any('Unreachable point' in m for m in messages))

    def test_get_version(self) -> None:
        '''
            Verifies validator get_version method returns semantic version string.
        '''
        validator = ScriptValidator(
            dependencies=ValidatorDependencies(
                parser=MagicMock(),
                linter=MagicMock(),
                compiler=MagicMock(),
            )
        )
        self.assertEqual(validator.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
