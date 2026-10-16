# -*- coding: UTF-8 -*-

'''
Module
    exporter_test.py
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
    Unit test cases for ScaraPlanExporter formatting and serializing.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.scara.exporter import ScaraPlanExporter
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraPlanExporter(TestCase):
    '''Test suite validating ScaraPlanExporter serialization logic.'''

    def setUp(self) -> None:
        '''Initializes exporter instance under test.'''
        self.exporter = ScaraPlanExporter()

    def test_format_waypoint_initial(self) -> None:
        '''Verifies formatting initial waypoint as MOVE_J.'''
        wp = Waypoint(
            name='START',
            x=100.0,
            y=150.0,
            z=20.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=True)
        self.assertTrue(line.startswith('MOVE_J'))
        self.assertIn('X=100.00', line)
        self.assertIn('Y=150.00', line)
        self.assertIn('Z=20.00', line)
        self.assertIn('PHI=0.00', line)
        self.assertIn('# START', line)

    def test_format_waypoint_linear(self) -> None:
        '''Verifies formatting non-initial waypoint as MOVE_L with speed.'''
        wp = Waypoint(
            name='NEXT',
            x=120.0,
            y=160.0,
            z=25.0,
            phi=10.0,
            speed=50.0,
            command='',
        )
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=False)
        self.assertTrue(line.startswith('MOVE_L'))
        self.assertIn('SPEED=50.0', line)
        self.assertIn('# NEXT', line)

    def test_format_joint_waypoint(self) -> None:
        '''Verifies format_waypoint with is_initial=True produces MOVE_J without flags.'''
        wp = Waypoint(
            name='START',
            x=100.0,
            y=150.0,
            z=20.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=True)
        self.assertTrue(line.startswith('MOVE_J'))
        self.assertIn('X=100.00', line)

    def test_format_linear_waypoint(self) -> None:
        '''Verifies format_waypoint with is_initial=False produces MOVE_L with speed.'''
        wp = Waypoint(
            name='NEXT',
            x=120.0,
            y=160.0,
            z=25.0,
            phi=10.0,
            speed=50.0,
            command='',
        )
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=False)
        self.assertTrue(line.startswith('MOVE_L'))
        self.assertIn('SPEED=50.0', line)

    def test_format_command_waypoint_delegation(self) -> None:
        '''Verifies format_waypoint delegates to command formatting when command is set.'''
        wp = Waypoint(name='PUMP_ON', x=0.0, y=0.0, z=0.0, phi=0.0, speed=0.0, command='<CMD:PUMP#1>')
        line_joint = self.exporter.format_waypoint(waypoint=wp, is_initial=True)
        line_linear = self.exporter.format_waypoint(waypoint=wp, is_initial=False)
        self.assertEqual(line_joint, 'PUMP ON')
        self.assertEqual(line_linear, 'PUMP ON')

    def test_export_plan_empty(self) -> None:
        '''Verifies exporting empty plan returns placeholder message.'''
        plan = TrajectoryPlan()
        output = self.exporter.export_plan(plan=plan)
        self.assertIn('# Empty trajectory plan', output)

    def test_export_plan_with_waypoints(self) -> None:
        '''Verifies exporting populated plan produces valid SCARA script.'''
        wp1 = Waypoint(
            name='HOME',
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        wp2 = Waypoint(
            name='POINT',
            x=50.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=60.0,
            command='',
        )
        plan = TrajectoryPlan()
        plan.add_point(wp1)
        plan.add_point(wp2)
        output = self.exporter.export_plan(plan=plan)
        self.assertIn('CONFIG ELBOW RIGHT', output)
        self.assertIn('MOVE_J', output)
        self.assertIn('MOVE_L', output)

    def test_export_scara(self) -> None:
        '''Verifies export_scara produces identical output as export_plan.'''
        wp = Waypoint(
            name='START',
            x=100.0,
            y=150.0,
            z=20.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        plan = TrajectoryPlan()
        plan.add_point(wp)
        self.assertEqual(
            self.exporter.export_scara(plan=plan),
            self.exporter.export_plan(plan=plan),
        )

    def test_format_command_waypoints(self) -> None:
        '''Verifies decoding and formatting non-motion command waypoints.'''
        cases = [
            ('<CMD:PUMP#1>', 'PUMP_ON', 'PUMP ON'),
            ('<CMD:PUMP#0>', 'PUMP_OFF', 'PUMP OFF'),
            ('<CMD:VALVE#1>', 'VALVE_ON', 'VALVE ON'),
            ('<CMD:VALVE#0>', 'VALVE_OFF', 'VALVE OFF'),
            ('<CMD:WAIT#500>', 'WAIT_500MS', 'WAIT 500'),
            ('<CMD:HOME>', 'HOME', 'HOME'),
            ('<CMD:CONFIG_MOTOR#OPEN_LOOP>', 'CONFIG_MOTOR', 'CONFIG MOTOR OPEN_LOOP'),
        ]
        for cmd_token, name, expected_prefix in cases:
            wp = Waypoint(
                name=name,
                x=0.0,
                y=0.0,
                z=0.0,
                phi=0.0,
                speed=0.0,
                command=cmd_token,
            )
            line = self.exporter.format_waypoint(waypoint=wp)
            self.assertTrue(
                line.startswith(expected_prefix),
                f'Expected line to start with {expected_prefix!r}, got {line!r}',
            )

    def test_export_plan_with_commands_and_moves(self) -> None:
        '''Verifies exporting plan preserves non-motion commands in sequence.'''
        wp_home = Waypoint(
            name='HOME',
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=0.0,
            command='<CMD:HOME>',
        )
        wp_move = Waypoint(
            name='TARGET',
            x=50.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=60.0,
            command='',
        )
        wp_pump = Waypoint(
            name='PUMP_ON',
            x=50.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=0.0,
            command='<CMD:PUMP#1>',
        )
        plan = TrajectoryPlan()
        plan.add_point(wp_home)
        plan.add_point(wp_move)
        plan.add_point(wp_pump)

        output = self.exporter.export_plan(plan=plan)
        lines = [line.strip() for line in output.splitlines() if line.strip() and not line.startswith('#')]
        self.assertIn('HOME', lines)
        self.assertIn('MOVE_J X=50.00 Y=50.00 Z=10.00 PHI=0.00  # TARGET', lines)
        self.assertIn('PUMP ON', lines)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)
