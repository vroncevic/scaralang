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
    Root factory for the SCARA DSL subsystem wiring parser, compiler, and binary pipeline.
'''

from __future__ import annotations

from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.core.service.dsl.binary.binary_service_factory import BinaryServiceFactory
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.dsl.scara_dsl_bundle import ScaraDslBundle
from scaralang.core.service.dsl.compilation.scara_dsl_compiler_factory import ScaraDslCompilerFactory
from scaralang.core.service.dsl.scara_dsl_pipeline_bundle import ScaraDslPipelineBundle
from scaralang.core.service.dsl.scara_dsl_service import ScaraDslService
from scaralang.core.service.dsl.toolchain.toolchain_info_provider_factory import ToolchainInfoProviderFactory
from scaralang.core.service.dsl.validation.scara_script_validator_factory import ScaraScriptValidatorFactory
from scaralang.core.service.exporter.scara.scara_plan_exporter_factory import ScaraPlanExporterFactory
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.linter.scara_linter_factory import ScaraLinterFactory
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser_factory import ScaraParserFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

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
                | create - Builds ScaraDslService from injected pipeline dependencies.
                | create_default - Builds ScaraDslService with standard kinematics defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, bundle: ScaraDslPipelineBundle) -> IScaraDslService:
        '''
            Builds ScaraDslService from injected pipeline dependencies.

            :param bundle: Injected ScaraDslPipelineBundle dependency container.
            :return: Fully wired IScaraDslService protocol instance.
            :exceptions: None.
        '''
        parser = ScaraParserFactory.create(lexer=ScaraLexerFactory.create())
        compiler = ScaraCompilerFactory.create(validator=bundle.validator)
        linter = ScaraLinterFactory.create()

        dsl_compiler = ScaraDslCompilerFactory.create(
            parser=parser,
            compiler=compiler,
            linter=linter,
        )
        script_validator = ScaraScriptValidatorFactory.create(
            parser=parser,
            compiler=compiler,
            linter=linter,
        )

        binary_service = BinaryServiceFactory.create_default(bundle=bundle)

        dsl_bundle = ScaraDslBundle(
            compiler=dsl_compiler,
            validator=script_validator,
            exporter=ScaraPlanExporterFactory.create(),
            binary_service=binary_service,
            toolchain_info=ToolchainInfoProviderFactory.create(),
        )

        return ScaraDslService(bundle=dsl_bundle)

    @classmethod
    def create_default(
        cls,
        *,
        frame_builder: IBinaryFrameBuilder,
        frame_parser: IBinaryFrameParser,
        payload_unpacker: IBinaryPayloadUnpacker,
    ) -> IScaraDslService:
        '''
            Builds and wires ScaraDslService using standard robotic kinematics defaults.

            :param frame_builder: Injected IBinaryFrameBuilder protocol instance.
            :param frame_parser: Injected IBinaryFrameParser protocol instance.
            :param payload_unpacker: Injected IBinaryPayloadUnpacker protocol instance.
            :return: Fully wired IScaraDslService protocol instance.
            :exceptions: None.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        transmission = DefaultScaraProfile.create_transmission()
        bundle = ScaraDslPipelineBundle(
            frame_builder=frame_builder,
            frame_parser=frame_parser,
            payload_unpacker=payload_unpacker,
            kinematics=kinematics,
            validator=validator,
            transmission=transmission,
        )

        return cls.create(bundle=bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
