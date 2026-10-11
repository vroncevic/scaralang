# -*- coding: UTF-8 -*-

'''
Module
    linter_test.py
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
    Unit tests for ScriptLinter class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.service.linter.script.dependencies import ScriptDependencies
from scaralang.core.service.linter.script.linter import ScriptLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScriptLinter(TestCase):
    '''
        Test cases verifying ScriptLinter operations.

        It defines:

            :methods:
                | test_lint_script_success - Verifies linting returns diagnostics.
                | test_lint_script_syntax_error - Verifies handling of parser exception.
                | test_lint_script_scara_syntax - Verifies SYNTAX_ERROR on ScaraSyntaxError.
                | test_lint_script_scara_semantic - Verifies SEMANTIC_ERROR on ScaraSemanticError.
                | test_lint_script_scara_kinematics - Verifies KINEMATICS_ERROR on kinematic error.
                | test_lint_script_scara_error - Verifies SYNTAX_ERROR on generic ScaraError.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_lint_script_success(self) -> None:
        '''
            Verifies lint_script returns diagnostics from injected linter.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_program = ScaraProgram(instructions=())
        mock_parser.parse.return_value = mock_program
        expected_diag = ScaraDiagnostic(
            code='SCARA_W001',
            severity=ScaraDiagnosticSeverity.WARNING,
            message='Calibration recommended',
            line=1,
            command='MOVE',
        )
        mock_linter.lint.return_value = (expected_diag,)

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='MOVE X10 Y20 Z0')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SCARA_W001')

    def test_lint_script_syntax_error(self) -> None:
        '''
            Verifies lint_script returns diagnostic on parser ValueError.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ValueError('Unexpected token: FOO')

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='FOO BAR')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SYNTAX_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertIn('Unexpected token', diagnostics[0].message)

    def test_lint_script_scara_syntax(self) -> None:
        '''
            Verifies lint_script assigns SYNTAX_ERROR for ScaraSyntaxError.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ScaraSyntaxError('Bad token sequence')

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='BAD')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SYNTAX_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)

    def test_lint_script_scara_semantic(self) -> None:
        '''
            Verifies lint_script assigns SEMANTIC_ERROR for ScaraSemanticError.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ScaraSemanticError('Undefined pallet PAL1')

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='MOVE_PALLET PAL1')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SEMANTIC_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)

    def test_lint_script_scara_kinematics(self) -> None:
        '''
            Verifies lint_script assigns KINEMATICS_ERROR for ScaraKinematicsError.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ScaraKinematicsError('Singularity deadband')

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='MOVE X0 Y0 Z0')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'KINEMATICS_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)

    def test_lint_script_scara_error(self) -> None:
        '''
            Verifies lint_script falls back to SYNTAX_ERROR for base ScaraError.
        '''
        mock_parser = MagicMock()
        mock_linter = MagicMock()
        mock_parser.parse.side_effect = ScaraError('Generic domain error')

        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=mock_parser,
                linter=mock_linter,
            )
        )
        diagnostics = service.lint_script(source='GENERIC')
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, 'SYNTAX_ERROR')
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)

    def test_get_version(self) -> None:
        '''
            Verifies linter get_version method returns semantic version string.
        '''
        service = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=MagicMock(),
                linter=MagicMock(),
            )
        )
        self.assertEqual(service.get_version(), '1.0.8')


if __name__ == '__main__':
    main()
