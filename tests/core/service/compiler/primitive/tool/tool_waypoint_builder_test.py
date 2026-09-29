# -*- coding: UTF-8 -*-

'''
Module
    tool_waypoint_builder_test.py
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
    Unit tests for ToolWaypointBuilder implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.primitive.tool.itool_waypoint_builder import IToolWaypointBuilder
from scaralang.core.service.compiler.primitive.tool.tool_waypoint_builder import ToolWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolWaypointBuilder(TestCase):
    '''
        Test cases verifying ToolWaypointBuilder functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_protocol_conformance - Verifies IToolWaypointBuilder conformance.
                | test_build_pump_on - Verifies waypoint construction for PUMP ON.
                | test_build_pump_off - Verifies waypoint construction for PUMP OFF.
                | test_build_valve_on - Verifies waypoint construction for VALVE ON.
                | test_build_valve_off - Verifies waypoint construction for VALVE OFF.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with context and builder instance.
        '''
        self.builder = ToolWaypointBuilder()
        self.context = ScaraCompilerContext()
        self.context.current_x = 120.0
        self.context.current_y = 60.0
        self.context.current_z = -15.0
        self.context.current_phi = 45.0
        self.context.current_speed = 80.0

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IToolWaypointBuilder.
        '''
        self.assertIsInstance(self.builder, IToolWaypointBuilder)

    def test_build_pump_on(self) -> None:
        '''
            Verifies waypoint generation for PUMP ON.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            tool_type=ScaraCommandType.PUMP,
            state=PneumaticState.ON,
        )
        self.assertEqual(waypoint.name, 'PUMP_ON')
        self.assertEqual(waypoint.command, '<CMD:PUMP#1>')
        self.assertEqual(waypoint.x, 120.0)
        self.assertEqual(waypoint.y, 60.0)
        self.assertEqual(waypoint.z, -15.0)
        self.assertEqual(waypoint.phi, 45.0)
        self.assertEqual(waypoint.speed, 80.0)

    def test_build_pump_off(self) -> None:
        '''
            Verifies waypoint generation for PUMP OFF.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            tool_type=ScaraCommandType.PUMP,
            state=PneumaticState.OFF,
        )
        self.assertEqual(waypoint.name, 'PUMP_OFF')
        self.assertEqual(waypoint.command, '<CMD:PUMP#0>')

    def test_build_valve_on(self) -> None:
        '''
            Verifies waypoint generation for VALVE ON.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            tool_type=ScaraCommandType.VALVE,
            state=PneumaticState.ON,
        )
        self.assertEqual(waypoint.name, 'VALVE_ON')
        self.assertEqual(waypoint.command, '<CMD:VALVE#1>')

    def test_build_valve_off(self) -> None:
        '''
            Verifies waypoint generation for VALVE OFF.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            tool_type=ScaraCommandType.VALVE,
            state=PneumaticState.OFF,
        )
        self.assertEqual(waypoint.name, 'VALVE_OFF')
        self.assertEqual(waypoint.command, '<CMD:VALVE#0>')


if __name__ == '__main__':
    main()
