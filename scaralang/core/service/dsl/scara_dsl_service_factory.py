# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service_factory.py
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
    Root factory for the SCARA DSL subsystem wiring lexer, parser, compiler, and binary pipeline.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scaralang.core.service.dsl.binary.command.command_compiler_factory import CommandCompilerFactory
from scaralang.core.service.dsl.binary.compiler_factory import CompilerFactory
from scaralang.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.dsl.binary.icompiler import ICompiler
from scaralang.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scaralang.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer
from scaralang.core.service.dsl.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scaralang.core.service.dsl.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scaralang.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.dsl.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.core.service.dsl.exporter.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.dsl.exporter.scara_plan_exporter_factory import ScaraPlanExporterFactory
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scaralang.core.service.dsl.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.dsl.parser.iscara_parser import IScaraParser
from scaralang.core.service.dsl.parser.scara_parser_factory import ScaraParserFactory
from scaralang.core.service.dsl.scara_dsl_service import ScaraDslService
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'

__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslServiceFactory:
    '''
        Factory providing composite composition for ScaraDslService using explicit sub-factory DI.

        It defines:

            :methods:
                | create - Wires child factories and returns an IScaraDslService instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: ITrajectoryValidator,
        kinematics: IKinematicsService,
        transmission: TransmissionParameters
    ) -> IScaraDslService:
        '''
            Builds and wires ScaraDslService performing explicit DI into child sub-factories.

            :param validator: Injected ITrajectoryValidator protocol instance.
            :param kinematics: Injected IKinematicsService protocol instance.
            :param transmission: Injected TransmissionParameters domain model.
            :return: Fully wired IScaraDslService protocol instance.
            :exceptions: None.
        '''
        active_lexer: IScaraLexer = ScaraLexerFactory.create()
        active_parser: IScaraParser = ScaraParserFactory.create(lexer=active_lexer)
        active_compiler: IScaraCompiler = ScaraCompilerFactory.create(validator=validator)
        active_exporter: IScaraPlanExporter = ScaraPlanExporterFactory.create()
        active_discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            kinematics=kinematics, transmission=transmission
        )
        active_frame_builder: IBinaryFrameBuilder = (BinaryFrameBuilderFactory.create())
        active_motion_compiler: IMotionCompiler = MotionCompilerFactory.create(
            discretizer=active_discretizer, frame_builder=active_frame_builder
        )
        active_command_compiler: ICommandCompiler = CommandCompilerFactory.create(
            frame_builder=active_frame_builder
        )
        active_binary_compiler: ICompiler = CompilerFactory.create(
            lexer=active_lexer,
            parser=active_parser,
            compiler=active_compiler,
            motion_compiler=active_motion_compiler,
            command_compiler=active_command_compiler
        )

        return ScaraDslService(
            lexer=active_lexer,
            parser=active_parser,
            compiler=active_compiler,
            exporter=active_exporter,
            binary_compiler=active_binary_compiler
        )

    @classmethod
    def create_default(cls) -> IScaraDslService:
        '''
            Builds and wires ScaraDslService using standard robotic kinematics defaults.

            :return: Fully wired IScaraDslService protocol instance.
            :exceptions: None.
        '''
        bounds = ScaraBounds(
            l1=150.0,
            l2=150.0,
            z_min=-50.0,
            z_max=50.0,
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
            j1_min_rad=-2.61799,
            j1_max_rad=2.61799,
            j2_min_rad=-2.61799,
            j2_max_rad=2.61799,
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0
        )
        kinematics: IKinematicsService = KinematicsServiceFactory.create(bounds=bounds)
        validator: ITrajectoryValidator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        transmission = TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=2.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0
        )
        return cls.create(validator=validator, kinematics=kinematics, transmission=transmission)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__

