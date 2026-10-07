# -*- coding: UTF-8 -*-

'''
Module
    primitive_instruction_processor_test.py
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
    Unit tests for PrimitiveInstructionProcessor.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.service.compiler.iprimitive_instruction_processor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.tool.tool_command_compiler_factory import ToolCommandCompilerFactory
from scaralang.core.service.compiler.primitive_instruction_processor import PrimitiveInstructionProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPrimitiveInstructionProcessor(TestCase):
    '''
        Test cases verifying PrimitiveInstructionProcessor execution and error handling.

        It defines:

            :methods:
                | setUp - Initializes processor with tool compiler.
                | test_structural_conformance - Verifies protocol check.
                | test_process_matched_instruction - Tests successful compilation.
                | test_process_unmatched_instruction - Tests ValueError on unhandled instruction.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.
        '''
        self.compiler: IPrimitiveCompiler = ToolCommandCompilerFactory.create()
        self.processor = PrimitiveInstructionProcessor(
            primitive_compilers=[self.compiler]
        )
        self.context = ScaraCompilerContext()

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IPrimitiveInstructionProcessor.
        '''
        self.assertIsInstance(self.processor, IPrimitiveInstructionProcessor)

    def test_get_version(self) -> None:
        '''
            Verifies processor get_version returns semantic version string.
        '''
        self.assertEqual(self.processor.get_version(), '1.0.7')

    def test_process_matched_instruction(self) -> None:
        '''
            Verifies that matched instruction compiles into waypoints.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            parameters={'STATE': PneumaticState.ON},
            line_number=1,
            raw_text='PUMP ON',
        )
        result = self.processor.process_primitive(
            instruction=instruction,
            context=self.context,
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, 'PUMP_ON')

    def test_process_unmatched_instruction(self) -> None:
        '''
            Verifies that unhandled instruction raises ScaraSemanticError.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={'X': 100.0, 'Y': 100.0},
            line_number=2,
            raw_text='MOVE_L X=100 Y=100',
        )
        with self.assertRaises(ScaraSemanticError):
            self.processor.process_primitive(
                instruction=instruction,
                context=self.context,
            )


if __name__ == '__main__':
    main()
