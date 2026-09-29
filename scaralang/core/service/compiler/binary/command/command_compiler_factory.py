# -*- coding: UTF-8 -*-

'''
Module
    command_compiler_factory.py
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
    Factory service providing wired CommandCompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.command.command_compiler import CommandCompiler
from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.compiler.binary.command.motor.imotor_frame_builder import IMotorFrameBuilder
from scaralang.core.service.compiler.binary.command.motor.motor_frame_builder_factory import MotorFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.tokens.command_token_parser_factory import CommandTokenParserFactory
from scaralang.core.service.compiler.binary.command.tokens.icommand_token_parser import ICommandTokenParser
from scaralang.core.service.compiler.binary.command.tool.itool_frame_builder import IToolFrameBuilder
from scaralang.core.service.compiler.binary.command.tool.tool_frame_builder_factory import ToolFrameBuilderFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandCompilerFactory:
    '''
        Factory providing configured ICommandCompiler instances.

        It defines:

            :methods:
                | create - Instantiates a new ICommandCompiler with wired builders.
                | create_with_collaborators - Instantiates with injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        frame_builder: IBinaryFrameBuilder,
    ) -> ICommandCompiler:
        '''
            Instantiates a new ICommandCompiler with wired frame builders.

            :param frame_builder: Injected IBinaryFrameBuilder instance.
            :return: Wired ICommandCompiler instance.
            :exceptions: None.
        '''
        tool_frame_builder: IToolFrameBuilder = (
            ToolFrameBuilderFactory.create(frame_builder=frame_builder)
        )
        motor_frame_builder: IMotorFrameBuilder = (
            MotorFrameBuilderFactory.create(frame_builder=frame_builder)
        )
        token_parser: ICommandTokenParser = CommandTokenParserFactory.create()

        return CommandCompiler(
            frame_builder=frame_builder,
            tool_frame_builder=tool_frame_builder,
            motor_frame_builder=motor_frame_builder,
            token_parser=token_parser,
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        frame_builder: IBinaryFrameBuilder,
        tool_frame_builder: IToolFrameBuilder,
        motor_frame_builder: IMotorFrameBuilder,
        token_parser: ICommandTokenParser,
    ) -> ICommandCompiler:
        '''
            Instantiates CommandCompiler with injected collaborators.

            :param frame_builder: Injected IBinaryFrameBuilder instance.
            :param tool_frame_builder: Injected IToolFrameBuilder instance.
            :param motor_frame_builder: Injected IMotorFrameBuilder instance.
            :param token_parser: Injected ICommandTokenParser instance.
            :return: Configured ICommandCompiler instance.
            :exceptions: None.
        '''
        return CommandCompiler(
            frame_builder=frame_builder,
            tool_frame_builder=tool_frame_builder,
            motor_frame_builder=motor_frame_builder,
            token_parser=token_parser,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
