# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing default full-stack ScaraCompiler composition.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.command.dependencies import CommandDependencies
from scaralang.core.service.compiler.binary.command.factory import CommandFactory
from scaralang.core.service.compiler.binary.dependencies import BinaryDependencies
from scaralang.core.service.compiler.binary.factory import BinaryFactory
from scaralang.core.service.compiler.binary.metrics.factory import MetricsCalculatorFactory
from scaralang.core.service.compiler.binary.motion.dependencies import MotionDependencies
from scaralang.core.service.compiler.binary.motion.factory import MotionFactory
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.dispatcher.dependencies import DispatcherDependencies
from scaralang.core.service.compiler.binary.step.dispatcher.factory import WaypointStepDispatcherFactory
from scaralang.core.service.compiler.dependencies import CompilerDependencies
from scaralang.core.service.compiler.factory import CompilerFactory
from scaralang.core.service.compiler.icompiler import IScaraCompiler
from scaralang.core.service.compiler.plan.dependencies import PlanDependencies
from scaralang.core.service.compiler.plan.factory import PlanFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory
from scaralang.core.service.linter.factory import LinterFactory
from scaralang.infrastructure.parser.factory import DefaultParserFactory
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultCompilerFactory:
    '''
        Factory providing default full-stack ScaraCompiler composition.

        It defines:

            :methods:
                | create - Builds and returns an IScaraCompiler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IScaraCompiler:
        '''
            Builds and returns an IScaraCompiler with standard defaults.

            :return: Fully configured IScaraCompiler protocol instance.
            :exceptions: None.
        '''
        kinematics = DefaultKinematicsFactory.create().service
        transmission = DefaultScaraProfile.create_transmission()
        frame_builder = BinaryFrameBuilderFactory.create()

        transmission_converter = JointStepTransmissionConverterFactory.create(
            transmission=transmission
        )
        discretizer = StepDiscretizerFactory.create(
            dependencies=DiscretizerDependencies(
                kinematics=kinematics,
                transmission=transmission_converter,
            )
        )
        motion_subsystem = MotionFactory.create(
            dependencies=MotionDependencies(
                discretizer=discretizer,
                frame_builder=frame_builder,
            )
        )
        command_subsystem = CommandFactory.create(
            dependencies=CommandDependencies(frame_builder=frame_builder)
        )
        step_dispatcher = WaypointStepDispatcherFactory.create(
            dependencies=DispatcherDependencies(
                command_compiler=command_subsystem.compiler,
                motion_compiler=motion_subsystem.compiler,
            )
        )
        binary_subsystem = BinaryFactory.create(
            dependencies=BinaryDependencies(
                step_dispatcher=step_dispatcher,
                metrics_calculator=MetricsCalculatorFactory.create(),
            )
        )
        parser = DefaultParserFactory.create().parser
        linter = LinterFactory.create().linter
        plan_subsystem = PlanFactory.create(
            dependencies=PlanDependencies(
                validator=DefaultValidationFactory.create().validator,
                parser=parser,
                linter=linter,
            )
        )
        provides = CompilerFactory.create(
            dependencies=CompilerDependencies(
                compiler=plan_subsystem.script_compiler,
                binary_compiler=binary_subsystem.compiler,
            )
        )
        return provides.compiler

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
