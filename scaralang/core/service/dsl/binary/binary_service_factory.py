# -*- coding: UTF-8 -*-

'''
Module
    binary_service_factory.py
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
    Factory instantiating and wiring BinaryService instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.binary_compiler_factory import BinaryCompilerFactory
from scaralang.core.service.compiler.binary.command.command_compiler_factory import CommandCompilerFactory
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.binary.metrics.binary_metrics_calculator_factory import BinaryMetricsCalculatorFactory
from scaralang.core.service.compiler.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scaralang.core.service.compiler.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.waypoint_step_dispatcher_factory import WaypointStepDispatcherFactory
from scaralang.core.service.disassembler.frame_detail_decoder_factory import FrameDetailDecoderFactory
from scaralang.core.service.disassembler.iscara_disassembler import IScaraDisassembler
from scaralang.core.service.disassembler.scara_disassembler_factory import ScaraDisassemblerFactory
from scaralang.core.service.dsl.binary.binary_service import BinaryService
from scaralang.core.service.dsl.binary.ibinary_service import IBinaryService
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryServiceFactory:
    '''
        Factory providing wired IBinaryService instances.

        It defines:

            :methods:
                | create - Builds BinaryService from compiler and disassembler.
                | create_default - Builds BinaryService using default binary pipeline.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        compiler: IBinaryCompiler,
        disassembler: IScaraDisassembler,
    ) -> IBinaryService:
        '''
            Builds and returns an IBinaryService structural protocol instance.

            :param compiler: Injected IBinaryCompiler protocol instance.
            :param disassembler: Injected IScaraDisassembler protocol instance.
            :return: Fully wired IBinaryService protocol instance.
            :exceptions: None.
        '''
        return BinaryService(compiler=compiler, disassembler=disassembler)

    @classmethod
    def create_default(
        cls,
        *,
        bundle: ScaraDslPipelineBundle,
    ) -> IBinaryService:
        '''
            Builds and wires BinaryService using default binary compilation pipeline components.

            :param bundle: Injected ScaraDslPipelineBundle dependency container.
            :return: Fully wired IBinaryService protocol instance.
            :exceptions: None.
        '''
        transmission_converter = JointStepTransmissionConverterFactory.create(
            transmission=bundle.transmission
        )
        discretizer = StepDiscretizerFactory.create(
            kinematics=bundle.kinematics,
            transmission=transmission_converter,
        )
        motion_compiler = MotionCompilerFactory.create(
            discretizer=discretizer,
            frame_builder=bundle.frame_builder,
        )
        step_dispatcher = WaypointStepDispatcherFactory.create(
            command_compiler=CommandCompilerFactory.create(
                frame_builder=bundle.frame_builder
            ),
            motion_compiler=motion_compiler,
        )
        compiler = BinaryCompilerFactory.create(
            step_dispatcher=step_dispatcher,
            metrics_calculator=BinaryMetricsCalculatorFactory.create(),
        )
        disassembler = ScaraDisassemblerFactory.create(
            parser=bundle.frame_parser,
            detail_decoder=FrameDetailDecoderFactory.create(
                unpacker=bundle.payload_unpacker
            ),
        )
        return cls.create(compiler=compiler, disassembler=disassembler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
