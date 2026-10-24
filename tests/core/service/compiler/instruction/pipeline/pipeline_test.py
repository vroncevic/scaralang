# -*- coding: UTF-8 -*-

'''
Module
    pipeline_test.py
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
    Unit tests for InstructionPipeline.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.service.compiler.instruction.pipeline.dependencies import PipelineDependencies
from scaralang.core.service.compiler.instruction.pipeline.factory import PipelineFactory
from scaralang.core.service.compiler.instruction.pipeline.ipipeline import IInstructionPipeline
from scaralang.core.service.compiler.instruction.pipeline.pipeline import InstructionPipeline
from scaralang.core.service.compiler.instruction.processor.dependencies import ProcessorDependencies
from scaralang.core.service.compiler.instruction.processor.factory import ProcessorFactory
from scaralang.core.service.compiler.instruction.processor.iprocessor import IPrimitiveInstructionProcessor
from scaralang.core.service.compiler.macro.jump.factory import JumpMacroExpanderFactory
from scaralang.core.service.compiler.macro.repeat.factory import RepeatFactory
from scaralang.core.service.compiler.macro.subroutine.factory import SubroutineFactory
from scaralang.core.service.compiler.primitive.motion.factory import MotionCommandCompilerFactory
from scaralang.core.service.compiler.primitive.state.factory import StateCommandCompilerFactory
from scaralang.core.service.compiler.primitive.tool.factory import ToolCommandCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInstructionPipeline(TestCase):
    '''
        Test cases verifying InstructionPipeline execution and error handling.

        It defines:

            :methods:
                | test_pipeline_execution - Verifies instruction expansion and compilation.
                | test_pipeline_unsupported_instruction - Verifies error when no compiler matches.
                | test_pipeline_direct_instantiation - Verifies direct class instantiation.
                | test_pipeline_with_macro_expansion - Verifies macro expansion in pipeline.
                | test_get_version - Verifies pipeline get_version returns semantic version string.
    '''

    def test_pipeline_execution(self) -> None:
        '''
            Verifies pipeline compiles instructions into waypoints.

            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(
                compilers=(
                    StateCommandCompilerFactory.create(),
                    ToolCommandCompilerFactory.create(),
                )
            )
        )
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        pipeline = PipelineFactory.create(
            dependencies=PipelineDependencies(
                subroutine_expander=subroutine_expander,
                repeat_expander=repeat_expander,
                macro_expanders=(),
                processor=processor,
            )
        )
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.SPEED,
                parameters={
                    ScaraInstructionParam.MODE: SpeedMode.RAPID,
                    ScaraInstructionParam.SPEED: 100.0,
                },
                line_number=1,
                raw_text='SPEED RAPID 100.0',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.PUMP,
                parameters={ScaraInstructionParam.STATE: PneumaticState.ON},
                line_number=2,
                raw_text='PUMP ON',
            ),
        ]
        waypoints = pipeline.compile_instructions(instructions=instructions)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:PUMP#1>')

    def test_pipeline_unsupported_instruction(self) -> None:
        '''
            Verifies ScaraSemanticError on unhandled instruction.

            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(compilers=())
        )
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        pipeline = PipelineFactory.create(
            dependencies=PipelineDependencies(
                subroutine_expander=subroutine_expander,
                repeat_expander=repeat_expander,
                macro_expanders=(),
                processor=processor,
            )
        )
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
        ]
        with self.assertRaises(ScaraSemanticError):
            pipeline.compile_instructions(instructions=instructions)

    def test_pipeline_direct_instantiation(self) -> None:
        '''
            Verifies InstructionPipeline direct class instantiation.

            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(compilers=())
        )
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        pipeline = InstructionPipeline(
            subroutine_expander=subroutine_expander,
            repeat_expander=repeat_expander,
            macro_expanders=(),
            processor=processor,
        )
        self.assertIsInstance(pipeline, IInstructionPipeline)

    def test_pipeline_with_macro_expansion(self) -> None:
        '''
            Verifies pipeline expands macro instructions and compiles primitive sub-instructions.

            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(
                compilers=(MotionCommandCompilerFactory.create(),)
            )
        )
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        pipeline = PipelineFactory.create(
            dependencies=PipelineDependencies(
                subroutine_expander=subroutine_expander,
                repeat_expander=repeat_expander,
                macro_expanders=(JumpMacroExpanderFactory.create(),),
                processor=processor,
            )
        )
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.JUMP,
                parameters={
                    ScaraInstructionParam.X: 100.0,
                    ScaraInstructionParam.Y: 50.0,
                    ScaraInstructionParam.Z: 10.0,
                    ScaraInstructionParam.PHI: 0.0,
                    ScaraInstructionParam.ARCH_HEIGHT: 25.0,
                    ScaraInstructionParam.SPEED: 50.0,
                },
                line_number=1,
                raw_text='JUMP X=100.0 Y=50.0 Z=10.0 ARCH_HEIGHT=25.0 SPEED=50.0',
            ),
        ]
        waypoints = pipeline.compile_instructions(instructions=instructions)
        self.assertEqual(len(waypoints), 3)

    def test_get_version(self) -> None:
        '''
            Verifies pipeline get_version returns semantic version string.

            :exceptions: None.
        '''
        processor: IPrimitiveInstructionProcessor = ProcessorFactory.create(
            dependencies=ProcessorDependencies(compilers=())
        )
        subroutine_expander = SubroutineFactory.create().expander
        repeat_expander = RepeatFactory.create().expander
        pipeline = InstructionPipeline(
            subroutine_expander=subroutine_expander,
            repeat_expander=repeat_expander,
            macro_expanders=(),
            processor=processor,
        )
        self.assertEqual(pipeline.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
