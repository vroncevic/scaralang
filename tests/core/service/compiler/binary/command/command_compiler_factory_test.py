# -*- coding: UTF-8 -*-

'''
Module
    command_compiler_factory_test.py
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
    Unit tests for CommandCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.command_compiler_factory import CommandCompilerFactory
from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.compiler.binary.command.motor.imotor_frame_builder import IMotorFrameBuilder
from scaralang.core.service.compiler.binary.command.motor.motor_frame_builder_factory import MotorFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.tokens.command_token_parser_factory import CommandTokenParserFactory
from scaralang.core.service.compiler.binary.command.tokens.icommand_token_parser import ICommandTokenParser
from scaralang.core.service.compiler.binary.command.tool.itool_frame_builder import IToolFrameBuilder
from scaralang.core.service.compiler.binary.command.tool.tool_frame_builder_factory import ToolFrameBuilderFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandCompilerFactory(TestCase):
    '''
        Test cases verifying CommandCompilerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns ICommandCompiler.
                | test_create_with_collaborators - Verifies creation with collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates wired ICommandCompiler instance.
        '''
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        compiler: ICommandCompiler = CommandCompilerFactory.create(
            frame_builder=frame_builder
        )
        self.assertIsInstance(compiler, ICommandCompiler)

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies factory creates ICommandCompiler with explicit collaborators.
        '''
        frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        tool_builder: IToolFrameBuilder = ToolFrameBuilderFactory.create(
            frame_builder=frame_builder
        )
        motor_builder: IMotorFrameBuilder = MotorFrameBuilderFactory.create(
            frame_builder=frame_builder
        )
        token_parser: ICommandTokenParser = CommandTokenParserFactory.create()
        compiler: ICommandCompiler = (
            CommandCompilerFactory.create_with_collaborators(
                frame_builder=frame_builder,
                tool_frame_builder=tool_builder,
                motor_frame_builder=motor_builder,
                token_parser=token_parser,
            )
        )
        self.assertIsInstance(compiler, ICommandCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        version = CommandCompilerFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
