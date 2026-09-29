# -*- coding: UTF-8 -*-

'''
Module
    instruction_pipeline_test.py
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
    Unit tests for InstructionPipeline and InstructionPipelineFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.service.compiler.iinstruction_pipeline import IInstructionPipeline
from scaralang.core.service.compiler.instruction_pipeline import InstructionPipeline
from scaralang.core.service.compiler.instruction_pipeline_factory import InstructionPipelineFactory
from scaralang.core.service.compiler.primitive_instruction_processor_factory import PrimitiveInstructionProcessorFactory
from scaralang.core.service.compiler.primitive.state.state_command_compiler_factory import StateCommandCompilerFactory
from scaralang.core.service.compiler.primitive.tool.tool_command_compiler_factory import ToolCommandCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInstructionPipeline(TestCase):
    '''
        Test cases verifying InstructionPipeline and its factory.

        It defines:

            :methods:
                | test_pipeline_execution - Verifies instruction expansion and compilation.
                | test_pipeline_unsupported_instruction - Verifies error when no compiler matches.
                | test_pipeline_factory - Verifies factory instantiates pipeline.
                | test_pipeline_with_collaborators - Verifies direct collaborator instantiation.
    '''

    def test_pipeline_execution(self) -> None:
        '''Verifies pipeline compiles instructions into waypoints.'''
        pipeline = InstructionPipelineFactory.create(
            macro_expanders=(),
            primitive_compilers=(
                StateCommandCompilerFactory.create(),
                ToolCommandCompilerFactory.create(),
            ),
        )
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.SPEED,
                parameters={
                    InstructionParam.MODE: SpeedMode.RAPID,
                    InstructionParam.SPEED: 100.0,
                },
                line_number=1,
                raw_text='SPEED RAPID 100.0',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.PUMP,
                parameters={InstructionParam.STATE: PneumaticState.ON},
                line_number=2,
                raw_text='PUMP ON',
            ),
        ]
        waypoints = pipeline.compile_instructions(instructions=instructions)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:PUMP#1>')

    def test_pipeline_unsupported_instruction(self) -> None:
        '''Verifies ValueError on unhandled instruction.'''
        pipeline = InstructionPipelineFactory.create(
            macro_expanders=(),
            primitive_compilers=(),
        )
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
        ]
        with self.assertRaises(ValueError):
            pipeline.compile_instructions(instructions=instructions)

    def test_pipeline_factory(self) -> None:
        '''Verifies InstructionPipelineFactory creation and version.'''
        pipeline = InstructionPipelineFactory.create(
            macro_expanders=(),
            primitive_compilers=(),
        )
        self.assertIsInstance(pipeline, IInstructionPipeline)
        self.assertEqual(InstructionPipelineFactory.get_version(), '1.0.0')

    def test_pipeline_with_collaborators(self) -> None:
        '''Verifies InstructionPipeline instantiation with injected processor.'''
        processor = PrimitiveInstructionProcessorFactory.create(
            primitive_compilers=()
        )
        pipeline = InstructionPipeline(
            macro_expanders=(),
            processor=processor,
        )
        self.assertIsInstance(pipeline, IInstructionPipeline)


if __name__ == '__main__':
    main()
