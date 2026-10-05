# -*- coding: UTF-8 -*-

'''
Module
    tool_frame_builder_test.py
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
    Unit tests for ToolFrameBuilder.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.compiler.binary.command.tool.itool_frame_builder import IToolFrameBuilder
from scaralang.core.service.compiler.binary.command.tool.tool_frame_builder import ToolFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolFrameBuilder(TestCase):
    '''
        Test cases verifying ToolFrameBuilder functionality.

        It defines:

            :methods:
                | setUp - Initializes fixtures with frame builder.
                | test_structural_conformance - Verifies protocol check.
                | test_get_version - Verifies get_version returns valid version string.
                | test_build_tool_frame_pump_on - Verifies PUMP ON frame.
                | test_build_tool_frame_valve_off - Verifies VALVE OFF frame.
    '''

    def setUp(self) -> None:
        '''
            Sets up frame builder and tool frame builder fixtures.
        '''
        self.frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()
        self.tool_builder = ToolFrameBuilder(frame_builder=self.frame_builder)

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IToolFrameBuilder.
        '''
        self.assertIsInstance(self.tool_builder, IToolFrameBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.tool_builder.get_version(), '1.0.4')


    def test_build_tool_frame_pump_on(self) -> None:
        '''
            Verifies building binary frame for PUMP ON actuation.
        '''
        frame: BinaryFrame = self.tool_builder.build_tool_frame(
            tool_id=ToolId.PUMP,
            arg='ON',
            clean='PUMP ON',
            seq_num=1,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(frame.seq_num, 1)
        self.assertEqual(len(frame.payload), 2)
        self.assertEqual(frame.payload[0], int(ToolId.PUMP))
        self.assertEqual(frame.payload[1], 1)

    def test_build_tool_frame_valve_off(self) -> None:
        '''
            Verifies building binary frame for VALVE OFF actuation.
        '''
        frame: BinaryFrame = self.tool_builder.build_tool_frame(
            tool_id=ToolId.VALVE,
            arg='0',
            clean='VALVE 0',
            seq_num=2,
        )
        self.assertEqual(frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(frame.seq_num, 2)
        self.assertEqual(len(frame.payload), 2)
        self.assertEqual(frame.payload[0], int(ToolId.VALVE))
        self.assertEqual(frame.payload[1], 0)


if __name__ == '__main__':
    main()
