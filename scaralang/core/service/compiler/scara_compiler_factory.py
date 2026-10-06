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
    Factory instantiating ScaraCompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.binary_compiler_factory import BinaryCompilerFactory
from scaralang.core.service.compiler.binary.command.command_compiler_factory import CommandCompilerFactory
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.binary.metrics.binary_metrics_calculator_factory import BinaryMetricsCalculatorFactory
from scaralang.core.service.compiler.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scaralang.core.service.compiler.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.waypoint_step_dispatcher_factory import WaypointStepDispatcherFactory
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.compiler.plan.scara_plan_compiler_factory import ScaraPlanCompilerFactory
from scaralang.core.service.compiler.scara_compiler import ScaraCompiler
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompilerFactory:
    '''
        Factory providing ScaraCompiler service instances.

        It defines:

            :methods:
                | create - Instantiates ScaraCompiler with injected delegates.
                | create_default - Instantiates ScaraCompiler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        compiler: IScaraPlanCompiler,
        binary_compiler: IBinaryCompiler,
    ) -> IScaraCompiler:
        '''
            Instantiates a configured ScaraCompiler service.

            :param compiler: Required IScaraPlanCompiler protocol instance.
            :param binary_compiler: Required IBinaryCompiler protocol instance.
            :return: Fully configured IScaraCompiler protocol instance.
            :exceptions: None.
        '''
        return ScaraCompiler(
            compiler=compiler,
            binary_compiler=binary_compiler,
        )

    @classmethod
    def create_default(cls) -> IScaraCompiler:
        '''
            Builds and returns an IScaraCompiler with standard defaults.

            :return: Fully configured IScaraCompiler protocol instance.
            :exceptions: None.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        transmission = DefaultScaraProfile.create_transmission()
        frame_builder = BinaryFrameBuilderFactory.create()

        transmission_converter = JointStepTransmissionConverterFactory.create(
            transmission=transmission
        )
        discretizer = StepDiscretizerFactory.create(
            kinematics=kinematics,
            transmission=transmission_converter,
        )
        motion_compiler = MotionCompilerFactory.create(
            discretizer=discretizer,
            frame_builder=frame_builder,
        )
        step_dispatcher = WaypointStepDispatcherFactory.create(
            command_compiler=CommandCompilerFactory.create(
                frame_builder=frame_builder
            ),
            motion_compiler=motion_compiler,
        )
        binary_compiler = BinaryCompilerFactory.create(
            step_dispatcher=step_dispatcher,
            metrics_calculator=BinaryMetricsCalculatorFactory.create(),
        )
        plan_compiler = ScaraPlanCompilerFactory.create_default()

        return ScaraCompiler(
            compiler=plan_compiler,
            binary_compiler=binary_compiler,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
