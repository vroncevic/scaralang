# -*- coding: UTF-8 -*-

'''
Module
    compiler_dependencies_test.py
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
    Unit tests for CommandCompilerDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.actuator.dependencies import ActuatorDependencies
from scaralang.core.service.compiler.binary.command.actuator.factory import ActuatorFrameBuilderFactory
from scaralang.core.service.compiler.binary.command.compiler_dependencies import CommandCompilerDependencies
from scaralang.core.service.compiler.binary.command.tokens.factory import TokenParserFactory
from scaralang.core.service.compiler.binary.command.tool.dependencies import ToolDependencies
from scaralang.core.service.compiler.binary.command.tool.factory import ToolFrameBuilderFactory
from scaralang.infrastructure.protocol.binary.builder.factory import BuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandCompilerDependencies(TestCase):
    '''
        Test cases verifying CommandCompilerDependencies parameter bundle.

        It defines:

            :methods:
                | test_attributes - Verifies attributes encapsulation.
                | test_immutability - Verifies frozen dataclass behavior.
    '''

    def test_attributes(self) -> None:
        '''
            Verifies attributes on CommandCompilerDependencies.

            :exceptions: None.
        '''
        builder_provides = BuilderFactory.create()
        tool_fb = ToolFrameBuilderFactory.create(
            dependencies=ToolDependencies(
                frame_builder=builder_provides.actuator
            )
        )
        actuator_fb = ActuatorFrameBuilderFactory.create(
            dependencies=ActuatorDependencies(
                frame_builder=builder_provides.actuator
            )
        )
        parser = TokenParserFactory.create()

        deps = CommandCompilerDependencies(
            frame_builder=builder_provides.system,
            frame_packer=builder_provides.packer,
            tool_frame_builder=tool_fb,
            actuator_frame_builder=actuator_fb,
            token_parser=parser,
        )
        self.assertIs(deps.frame_builder, builder_provides.system)
        self.assertIs(deps.frame_packer, builder_provides.packer)
        self.assertIs(deps.tool_frame_builder, tool_fb)
        self.assertIs(deps.actuator_frame_builder, actuator_fb)
        self.assertIs(deps.token_parser, parser)

    def test_immutability(self) -> None:
        '''
            Verifies CommandCompilerDependencies is frozen.

            :exceptions: None.
        '''
        builder_provides = BuilderFactory.create()
        tool_fb = ToolFrameBuilderFactory.create(
            dependencies=ToolDependencies(
                frame_builder=builder_provides.actuator
            )
        )
        actuator_fb = ActuatorFrameBuilderFactory.create(
            dependencies=ActuatorDependencies(
                frame_builder=builder_provides.actuator
            )
        )
        parser = TokenParserFactory.create()

        deps = CommandCompilerDependencies(
            frame_builder=builder_provides.system,
            frame_packer=builder_provides.packer,
            tool_frame_builder=tool_fb,
            actuator_frame_builder=actuator_fb,
            token_parser=parser,
        )
        with self.assertRaises(AttributeError):
            deps.frame_builder = builder_provides.system  # type: ignore


if __name__ == '__main__':
    main()
