# -*- coding: UTF-8 -*-

'''
Module
    scara_linter_test.py
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
    Unit tests for ScaraLinter ahead-of-time static analysis and diagnostic checks.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity
from scaralang.core.service.linter.rules.timing.timing_lint_rule_factory import TimingLintRuleFactory
from scaralang.core.service.linter.scara_linter_factory import ScaraLinterFactory
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser_factory import ScaraParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraLinter(TestCase):
    '''
        Test cases verifying ahead-of-time static analysis in ScaraLinter.

        It defines:

            :methods:
                | setUp - Initializes lexer, parser, and linter instances.
                | test_rules_property - Verifies configured rules on default linter.
                | test_empty_program_error - Verifies ERROR on empty program AST.
                | test_pneumatic_conflict_error - Verifies ERROR on simultaneous pump and valve contention.
                | test_uncalibrated_motion_warning - Verifies WARNING on motion prior to homing.
                | test_tool_in_flyby_warning - Verifies WARNING on tool command during active zone blending.
                | test_redundant_tool_command_warning - Verifies WARNING on consecutive identical tool states.
                | test_dead_wait_info - Verifies INFO on non-positive dwell delay.
                | test_duplicate_motion_info - Verifies INFO on consecutive identical motion targets.
                | test_clean_program_no_diagnostics - Verifies zero diagnostics on fully compliant script.
                | test_custom_rule_injection - Verifies custom rule injection in linter.
                | test_invalid_zone_diagnostics - Verifies diagnostics on invalid zone mode and negative radius.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test execution.
        '''
        self._lexer = ScaraLexerFactory.create()
        self._parser = ScaraParserFactory.create(lexer=self._lexer)
        self._linter = ScaraLinterFactory.create()

    def test_rules_property(self) -> None:
        '''
            Verifies default linter contains four configured rules.
        '''
        self.assertEqual(len(self._linter.rules), 4)

    def parse_source(self, source: str) -> ScaraProgram:
        '''
            Helper parsing source code into a ScaraProgram AST.

            :param source: SCARA DSL source text.
            :return: ScaraProgram AST root.
        '''
        tokens = self._lexer.tokenize(source=source)
        return self._parser.parse_tokens(tokens=tokens)

    def test_empty_program_error(self) -> None:
        '''
            Verifies ERROR diagnostic on empty program AST.
        '''
        empty_prog = ScaraProgram(instructions=())
        diagnostics = self._linter.lint(program=empty_prog)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.EMPTY_PROGRAM)

    def test_pneumatic_conflict_error(self) -> None:
        '''
            Verifies ERROR on simultaneous pump and valve contention.
        '''
        source = (
            'HOME\n'
            'PUMP ON\n'
            'VALVE ON\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        conflict_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.PNEUMATIC_CONFLICT
        ]
        self.assertEqual(len(conflict_diags), 1)
        self.assertEqual(conflict_diags[0].severity, ScaraDiagnosticSeverity.ERROR)
        self.assertEqual(conflict_diags[0].line, 3)

    def test_uncalibrated_motion_warning(self) -> None:
        '''
            Verifies WARNING on motion prior to homing.
        '''
        source = 'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        uncal_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.UNCALIBRATED_MOTION
        ]
        self.assertEqual(len(uncal_diags), 1)
        self.assertEqual(uncal_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_tool_in_flyby_warning(self) -> None:
        '''
            Verifies WARNING on tool command during active zone blending.
        '''
        source = (
            'HOME\n'
            'ZONE BLEND R=10.0\n'
            'PUMP ON\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        flyby_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.TOOL_IN_FLYBY
        ]
        self.assertEqual(len(flyby_diags), 1)
        self.assertEqual(flyby_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_redundant_tool_command_warning(self) -> None:
        '''
            Verifies WARNING on consecutive identical tool states.
        '''
        source = (
            'HOME\n'
            'PUMP ON\n'
            'PUMP ON\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        redundant_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.REDUNDANT_TOOL_CMD
        ]
        self.assertEqual(len(redundant_diags), 1)
        self.assertEqual(redundant_diags[0].severity, ScaraDiagnosticSeverity.WARNING)

    def test_dead_wait_info(self) -> None:
        '''
            Verifies INFO on non-positive dwell delay.
        '''
        source = (
            'HOME\n'
            'WAIT_MS 0\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        wait_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.DEAD_WAIT
        ]
        self.assertEqual(len(wait_diags), 1)
        self.assertEqual(wait_diags[0].severity, ScaraDiagnosticSeverity.INFO)

    def test_duplicate_motion_info(self) -> None:
        '''
            Verifies INFO on consecutive identical motion targets.
        '''
        source = (
            'HOME\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        dup_diags = [
            d for d in diagnostics
            if d.code == ScaraDiagnosticCode.DUPLICATE_MOTION
        ]
        self.assertEqual(len(dup_diags), 1)
        self.assertEqual(dup_diags[0].severity, ScaraDiagnosticSeverity.INFO)

    def test_clean_program_no_diagnostics(self) -> None:
        '''
            Verifies zero diagnostics on fully compliant script.
        '''
        source = (
            'HOME\n'
            'MOVE_L X=150.0 Y=50.0 Z=20.0\n'
            'PUMP ON\n'
            'WAIT_MS 100\n'
            'MOVE_L X=160.0 Y=60.0 Z=20.0\n'
            'PUMP OFF\n'
        )
        program = self.parse_source(source)
        diagnostics = self._linter.lint(program=program)
        self.assertEqual(len(diagnostics), 0)

    def test_custom_rule_injection(self) -> None:
        '''
            Verifies ScaraLinter accepts customized sequence of rules.
        '''
        custom_rule = TimingLintRuleFactory.create_default()
        custom_linter = ScaraLinterFactory.create_with_rules(rules=(custom_rule,))
        source = 'MOVE_L X=150.0 Y=50.0 Z=20.0\nWAIT_MS -10\n'
        program = self.parse_source(source)
        diagnostics = custom_linter.lint(program=program)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0].code, ScaraDiagnosticCode.DEAD_WAIT)

    def test_invalid_zone_diagnostics(self) -> None:
        '''
            Verifies WARNING diagnostics on invalid zone mode and negative radius.
        '''
        prog = ScaraProgram(
            instructions=(
                ScaraInstruction(
                    command_type=ScaraCommandType.ZONE,
                    line_number=1,
                    raw_text='ZONE BLEND R=-5.0',
                    parameters={
                        InstructionParam.MODE: 'BLEND',
                        InstructionParam.RADIUS: -5.0,
                    },
                ),
                ScaraInstruction(
                    command_type=ScaraCommandType.ZONE,
                    line_number=2,
                    raw_text='ZONE FAST',
                    parameters={
                        InstructionParam.MODE: 'FAST',
                        InstructionParam.RADIUS: 0.0,
                    },
                ),
            )
        )
        diagnostics = self._linter.lint(program=prog)
        codes = [d.code for d in diagnostics]
        self.assertIn(ScaraDiagnosticCode.INVALID_ZONE_RADIUS, codes)
        self.assertIn(ScaraDiagnosticCode.INVALID_ZONE_MODE, codes)


if __name__ == '__main__':
    main()
