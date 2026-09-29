# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_compiler_test.py
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
    Unit tests for ScaraDslCompiler class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.dsl.compilation.scara_dsl_compiler import ScaraDslCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslCompiler(TestCase):
    '''
        Test cases verifying ScaraDslCompiler operations.

        It defines:

            :methods:
                | test_compile_program_success - Verifies compilation of AST program.
                | test_compile_program_with_errors - Verifies ValueError on linter errors.
                | test_compile_script_success - Verifies script parsing and compilation.
    '''

    def test_compile_program_success(self) -> None:
        '''
            Verifies compile_program passes when linter reports no errors.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        mock_linter.lint.return_value = ()
        mock_plan = MagicMock()
        mock_compiler.compile.return_value = mock_plan

        dsl_compiler = ScaraDslCompiler(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        plan = dsl_compiler.compile_program(program=program)
        self.assertEqual(plan, mock_plan)
        mock_compiler.compile.assert_called_once_with(program=program)

    def test_compile_program_with_errors(self) -> None:
        '''
            Verifies compile_program raises ValueError when linter finds errors.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        diag = ScaraDiagnostic(
            code='ERR_KINEMATICS',
            severity=ScaraDiagnosticSeverity.ERROR,
            message='Out of reach',
            line=1,
            command='MOVE',
        )
        mock_linter.lint.return_value = (diag,)

        dsl_compiler = ScaraDslCompiler(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        with self.assertRaises(ValueError) as ctx:
            dsl_compiler.compile_program(program=program)
        self.assertIn('Compilation aborted due to static analysis errors', str(ctx.exception))
        self.assertIn('Out of reach', str(ctx.exception))

    def test_compile_script_success(self) -> None:
        '''
            Verifies compile_script parses source and compiles program.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()

        program = ScaraProgram(instructions=())
        mock_parser.parse.return_value = program
        mock_linter.lint.return_value = ()
        mock_plan = MagicMock()
        mock_compiler.compile.return_value = mock_plan

        dsl_compiler = ScaraDslCompiler(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        plan = dsl_compiler.compile_script(source='MOVE X10 Y10 Z0')
        self.assertEqual(plan, mock_plan)
        mock_parser.parse.assert_called_once_with(source='MOVE X10 Y10 Z0')
        mock_compiler.compile.assert_called_once_with(program=program)


if __name__ == '__main__':
    main()
