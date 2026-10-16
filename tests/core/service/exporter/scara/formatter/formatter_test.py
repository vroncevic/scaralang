# -*- coding: UTF-8 -*-

'''
Module
    formatter_test.py
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
    Unit test cases for ScaraWaypointFormatter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.scara.formatter.factory import ScaraWaypointFormatterFactory
from scaralang.core.service.exporter.scara.formatter.formatter import ScaraWaypointFormatter
from scaralang.core.service.exporter.scara.formatter.iformatter import IScaraWaypointFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraWaypointFormatter(TestCase):
    '''
    Test cases verifying ScaraWaypointFormatter operations.

    It defines:

        :methods:
            | setUp - Sets up formatter fixture.
            | test_protocol_conformance - Verifies protocol check.
            | test_factory - Verifies factory creation.
            | test_format_motion_joint - Verifies rapid joint motion formatting.
            | test_format_motion_linear - Verifies linear motion formatting.
            | test_format_command_pump - Verifies pump command formatting.
            | test_format_command_valve - Verifies valve command formatting.
            | test_format_command_wait - Verifies wait command formatting.
            | test_format_command_motor - Verifies motor configuration formatting.
            | test_format_command_system - Verifies system commands formatting.
            | test_get_version - Verifies version string retrieval.
    '''

    def setUp(self) -> None:
        '''
        Sets up formatter fixture.
        '''
        self.formatter: ScaraWaypointFormatter = ScaraWaypointFormatter()

    def test_protocol_conformance(self) -> None:
        '''
        Verifies formatter satisfies IScaraWaypointFormatter protocol.
        '''
        self.assertIsInstance(self.formatter, IScaraWaypointFormatter)

    def test_factory(self) -> None:
        '''
        Verifies factory instantiates valid formatter.
        '''
        instance = ScaraWaypointFormatterFactory.create()
        self.assertIsInstance(instance, IScaraWaypointFormatter)
        self.assertEqual(ScaraWaypointFormatterFactory.get_version(), '1.0.9')

    def test_format_motion_joint(self) -> None:
        '''
        Verifies rapid joint motion formatting with MOVE_J.
        '''
        wp = Waypoint(
            name='START',
            x=100.0,
            y=150.0,
            z=20.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        line = self.formatter.format_waypoint(waypoint=wp, is_initial=True)
        self.assertTrue(line.startswith('MOVE_J'))
        self.assertIn('X=100.00', line)
        self.assertIn('Y=150.00', line)
        self.assertIn('Z=20.00', line)
        self.assertIn('PHI=0.00', line)
        self.assertIn('# START', line)

    def test_format_motion_linear(self) -> None:
        '''
        Verifies linear motion formatting with MOVE_L.
        '''
        wp = Waypoint(
            name='NEXT',
            x=120.0,
            y=160.0,
            z=25.0,
            phi=10.0,
            speed=50.0,
            command='',
        )
        line = self.formatter.format_waypoint(waypoint=wp, is_initial=False)
        self.assertTrue(line.startswith('MOVE_L'))
        self.assertIn('SPEED=50.0', line)
        self.assertIn('# NEXT', line)

    def test_format_command_pump(self) -> None:
        '''
        Verifies pump command formatting.
        '''
        wp_on = Waypoint(name='PUMP_ON', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:PUMP#1>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_on), 'PUMP ON')
        wp_off = Waypoint(name='PUMP_OFF', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:PUMP#0>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_off), 'PUMP OFF')

    def test_format_command_valve(self) -> None:
        '''
        Verifies valve command formatting.
        '''
        wp_on = Waypoint(name='VALVE_ON', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:VALVE#1>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_on), 'VALVE ON')
        wp_off = Waypoint(name='VALVE_OFF', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:VALVE#0>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_off), 'VALVE OFF')

    def test_format_command_wait(self) -> None:
        '''
        Verifies wait delay command formatting.
        '''
        wp = Waypoint(name='WAIT_500', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:WAIT#500>')
        self.assertEqual(self.formatter.format_command(waypoint=wp), 'WAIT 500')

    def test_format_command_motor(self) -> None:
        '''
        Verifies motor configuration command formatting.
        '''
        wp = Waypoint(name='CFG_MOTOR', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:CONFIG_MOTOR#CLOSED_LOOP>')
        self.assertEqual(self.formatter.format_command(waypoint=wp), 'CONFIG MOTOR CLOSED_LOOP  # CFG_MOTOR')

    def test_format_command_system(self) -> None:
        '''
        Verifies system commands formatting (HOME, HOLD, etc.).
        '''
        wp_home = Waypoint(name='HOME', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:HOME>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_home), 'HOME')
        wp_estop = Waypoint(name='ESTOP', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:ESTOP>')
        self.assertEqual(self.formatter.format_command(waypoint=wp_estop), 'ESTOP')
        wp_custom = Waypoint(name='CUSTOM', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='CUSTOM_OP')
        self.assertEqual(self.formatter.format_command(waypoint=wp_custom), 'CUSTOM_OP  # CUSTOM')

    def test_get_version(self) -> None:
        '''
        Verifies version string retrieval.
        '''
        self.assertEqual(self.formatter.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
