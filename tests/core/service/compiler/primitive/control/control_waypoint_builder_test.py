# -*- coding: UTF-8 -*-

'''
Module
    control_waypoint_builder_test.py
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
    Unit tests for ControlWaypointBuilder.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.compiler.control_waypoint_descriptor import ControlWaypointDescriptor
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.primitive.control.control_waypoint_builder import ControlWaypointBuilder
from scaralang.core.service.compiler.primitive.control.icontrol_waypoint_builder import IControlWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestControlWaypointBuilder(TestCase):
    '''
        Test cases verifying ControlWaypointBuilder functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_protocol_conformance - Verifies IControlWaypointBuilder conformance.
                | test_build_waypoint_context_defaults - Verifies waypoint with context coordinates.
                | test_build_waypoint_overridden_values - Verifies waypoint with custom phi and speed.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with context and builder instance.
        '''
        self.builder = ControlWaypointBuilder()
        self.context = ScaraCompilerContext()
        self.context.pose.current_x = 200.0
        self.context.pose.current_y = 100.0
        self.context.pose.current_z = 30.0
        self.context.pose.current_phi = 90.0
        self.context.speed.current_speed = 50.0

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IControlWaypointBuilder.
        '''
        self.assertIsInstance(self.builder, IControlWaypointBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies builder get_version returns semantic version string.
        '''
        self.assertEqual(self.builder.get_version(), '1.0.7')

    def test_build_waypoint_context_defaults(self) -> None:
        '''
            Verifies waypoint creation using context coordinates.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            descriptor=ControlWaypointDescriptor(
                name='HOLD',
                command='<CMD:HOLD>',
                phi=self.context.pose.current_phi,
                speed=self.context.speed.current_speed,
            ),
        )
        self.assertEqual(waypoint.name, 'HOLD')
        self.assertEqual(waypoint.command, '<CMD:HOLD>')
        self.assertEqual(waypoint.x, 200.0)
        self.assertEqual(waypoint.y, 100.0)
        self.assertEqual(waypoint.z, 30.0)
        self.assertEqual(waypoint.phi, 90.0)
        self.assertEqual(waypoint.speed, 50.0)

    def test_build_waypoint_overridden_values(self) -> None:
        '''
            Verifies waypoint creation with overridden phi and speed.
        '''
        waypoint = self.builder.build_waypoint(
            context=self.context,
            descriptor=ControlWaypointDescriptor(
                name='HOME',
                command='<CMD:HOME>',
                phi=0.0,
                speed=200.0,
            ),
        )
        self.assertEqual(waypoint.name, 'HOME')
        self.assertEqual(waypoint.command, '<CMD:HOME>')
        self.assertEqual(waypoint.phi, 0.0)
        self.assertEqual(waypoint.speed, 200.0)


if __name__ == '__main__':
    main()
