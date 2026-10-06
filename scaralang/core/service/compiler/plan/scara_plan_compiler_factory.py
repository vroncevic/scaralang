# -*- coding: UTF-8 -*-

'''
Module
    scara_plan_compiler_factory.py
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
    Factory instantiating and providing ScaraPlanCompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.compiler.plan.itrajectory_plan_compiler import ITrajectoryPlanCompiler
from scaralang.core.service.compiler.plan.scara_plan_compiler import ScaraPlanCompiler
from scaralang.core.service.compiler.plan.trajectory_plan_compiler_factory import TrajectoryPlanCompilerFactory
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.linter.iscara_linter import IScaraLinter
from scaralang.core.service.linter.scara_linter_factory import ScaraLinterFactory
from scaralang.core.service.parser.iscara_parser import IScaraParser
from scaralang.core.service.parser.lexer.scara_lexer_factory import ScaraLexerFactory
from scaralang.core.service.parser.scara_parser_factory import ScaraParserFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraPlanCompilerFactory:
    '''
        Factory providing ScaraPlanCompiler instances.

        It defines:

            :methods:
                | create - Builds and returns a ScaraPlanCompiler instance.
                | create_default - Builds and returns default ScaraPlanCompiler instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        parser: IScaraParser,
        compiler: ITrajectoryPlanCompiler,
        linter: IScaraLinter,
    ) -> IScaraPlanCompiler:
        '''
            Builds and returns a ScaraPlanCompiler instance.

            :param parser: Required IScaraParser protocol instance.
            :param compiler: Required ITrajectoryPlanCompiler protocol instance.
            :param linter: Required IScaraLinter protocol instance.
            :return: Configured IScaraPlanCompiler protocol instance.
            :exceptions: None.
        '''
        return ScaraPlanCompiler(
            parser=parser,
            compiler=compiler,
            linter=linter,
        )

    @classmethod
    def create_default(cls) -> IScaraPlanCompiler:
        '''
            Builds and returns a ScaraPlanCompiler with default configurations.

            :return: Fully configured IScaraPlanCompiler protocol instance.
            :exceptions: None.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        parser = ScaraParserFactory.create(lexer=ScaraLexerFactory.create())
        compiler = TrajectoryPlanCompilerFactory.create(validator=validator)
        linter = ScaraLinterFactory.create()

        return ScaraPlanCompiler(
            parser=parser,
            compiler=compiler,
            linter=linter,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
