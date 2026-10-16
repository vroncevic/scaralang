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
    Factory service assembling and providing command compilation subsystem.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.command.actuator.dependencies import ActuatorDependencies
from scaralang.core.service.compiler.binary.command.actuator.factory import ActuatorFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.actuator.ibuilder import IActuatorFrameBuilder
from scaralang.core.service.compiler.binary.command.compiler import CommandCompiler
from scaralang.core.service.compiler.binary.command.compiler_dependencies import CommandCompilerDependencies
from scaralang.core.service.compiler.binary.command.dependencies import CommandDependencies
from scaralang.core.service.compiler.binary.command.provides import CommandProvides
from scaralang.core.service.compiler.binary.command.tokens.factory import TokenParserFactory
from scaralang.core.service.compiler.binary.command.tokens.iparser import ITokenParser
from scaralang.core.service.compiler.binary.command.tool.dependencies import ToolDependencies
from scaralang.core.service.compiler.binary.command.tool.factory import ToolFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.tool.ibuilder import IToolFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFactory:
    '''
        Factory providing wired CommandProvides instances.

        It defines:

            :methods:
                | create - Instantiates and bundles all command compilation collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: CommandDependencies,
    ) -> CommandProvides:
        '''
            Instantiates and wires all command compilation collaborators into CommandProvides.

            :param dependencies: Parameter bundle with foreign collaborators.
            :return: Immutable CommandProvides container.
            :exceptions: None.
        '''
        tool_frame_builder: IToolFrameBuilder = (
            ToolFrameBuilderFactory.create(
                dependencies=ToolDependencies(
                    frame_builder=dependencies.actuator_builder
                )
            )
        )
        actuator_frame_builder: IActuatorFrameBuilder = (
            ActuatorFrameBuilderFactory.create(
                dependencies=ActuatorDependencies(
                    frame_builder=dependencies.actuator_builder
                )
            )
        )
        token_parser: ITokenParser = TokenParserFactory.create()

        compiler = CommandCompiler(
            dependencies=CommandCompilerDependencies(
                frame_builder=dependencies.system_builder,
                frame_packer=dependencies.frame_packer,
                tool_frame_builder=tool_frame_builder,
                actuator_frame_builder=actuator_frame_builder,
                token_parser=token_parser,
            )
        )

        return CommandProvides(compiler=compiler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
