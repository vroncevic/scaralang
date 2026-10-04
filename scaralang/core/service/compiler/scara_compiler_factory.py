# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_factory.py
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
    Factory instantiating and wiring ScaraCompiler with validators and instruction pipeline.
'''

from __future__ import annotations

from scaralang.core.service.compiler.iinstruction_pipeline import IInstructionPipeline
from scaralang.core.service.compiler.instruction_pipeline_factory import InstructionPipelineFactory
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.macro.frame_macro_expander_factory import FrameMacroExpanderFactory
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander
from scaralang.core.service.compiler.macro.itangent_macro_expander import ITangentMacroExpander
from scaralang.core.service.compiler.macro.jump_macro_expander_factory import JumpMacroExpanderFactory
from scaralang.core.service.compiler.macro.pallet_macro_expander_factory import PalletMacroExpanderFactory
from scaralang.core.service.compiler.macro.tangent_macro_expander_factory import TangentMacroExpanderFactory
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator_factory import ArcInterpolatorFactory
from scaralang.core.service.compiler.motion.motion_command_compiler_factory import MotionCommandCompilerFactory
from scaralang.core.service.compiler.primitive.control.control_command_compiler_factory import ControlCommandCompilerFactory
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.state.state_command_compiler_factory import StateCommandCompilerFactory
from scaralang.core.service.compiler.primitive.tool.tool_command_compiler_factory import ToolCommandCompilerFactory
from scaralang.core.service.compiler.scara_compiler import ScaraCompiler
from scaralang.core.service.trajectory.plan.itrajectory_plan_factory import ITrajectoryPlanFactory
from scaralang.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompilerFactory:
    '''
        Factory providing wired IScaraCompiler instances.

        It defines:

            :methods:
                | create - Builds and wires ScaraCompiler with collaborators.
                | create_with_collaborators - Builds ScaraCompiler with injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: ITrajectoryValidator,
    ) -> IScaraCompiler:
        '''
            Builds and wires ScaraCompiler with internal collaborators.

            :param validator: Injected ITrajectoryValidator instance.
            :return: IScaraCompiler structural protocol instance.
            :exceptions: None.
        '''
        active_tangent: ITangentMacroExpander = TangentMacroExpanderFactory.create()
        active_motion = MotionCommandCompilerFactory.create_with_helpers(
            tangent_helper=active_tangent,
            arc_interpolator=ArcInterpolatorFactory.create(),
        )

        active_expanders: tuple[IMacroExpander, ...] = (
            JumpMacroExpanderFactory.create(),
            FrameMacroExpanderFactory.create(),
            PalletMacroExpanderFactory.create(),
            active_tangent,
        )

        active_compilers: tuple[IPrimitiveCompiler, ...] = (
            StateCommandCompilerFactory.create(),
            ToolCommandCompilerFactory.create(),
            ControlCommandCompilerFactory.create(),
            active_motion,
        )

        pipeline = InstructionPipelineFactory.create(
            macro_expanders=active_expanders,
            primitive_compilers=active_compilers,
        )

        return ScaraCompiler(
            validator=validator,
            instruction_pipeline=pipeline,
            plan_factory=TrajectoryPlanFactory(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        validator: ITrajectoryValidator,
        instruction_pipeline: IInstructionPipeline,
        plan_factory: ITrajectoryPlanFactory,
    ) -> IScaraCompiler:
        '''
            Builds ScaraCompiler with injected collaborators.

            :param validator: Injected ITrajectoryValidator instance.
            :param instruction_pipeline: Injected IInstructionPipeline instance.
            :param plan_factory: Injected ITrajectoryPlanFactory instance.
            :return: IScaraCompiler structural protocol instance.
            :exceptions: None.
        '''
        return ScaraCompiler(
            validator=validator,
            instruction_pipeline=instruction_pipeline,
            plan_factory=plan_factory,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
