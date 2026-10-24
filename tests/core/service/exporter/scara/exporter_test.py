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
    Unit test cases for ScaraPlanExporter class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.exporter.scara.exporter import ScaraPlanExporter
from scaralang.core.service.exporter.scara.formatter.factory import ScaraWaypointFormatterFactory
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraPlanExporter(TestCase):
    '''
        Unit tests for ScaraPlanExporter export operations.

        It defines:

            :attributes:
                | exporter - ScaraPlanExporter instance under test.
            :methods:
                | setUp - Initializes exporter instance under test.
                | test_export_plan_empty - Verifies exporting empty plan returns fallback comment.
                | test_export_plan_with_waypoints - Verifies exporting populated plan produces SCARA script.
                | test_export_plan_with_commands_and_moves - Verifies commands and moves in sequence.
                | test_get_version - Verifies version string reporting.
    '''

    def setUp(self) -> None:
        '''
            Initializes exporter instance under test.

            :exceptions: None.
        '''
        self.exporter: ScaraPlanExporter = ScaraPlanExporter(
            formatter=ScaraWaypointFormatterFactory.create()
        )

    def test_export_plan_empty(self) -> None:
        '''
            Verifies exporting empty plan returns placeholder message.

            :exceptions: None.
        '''
        plan = TrajectoryPlan(waypoints=())
        output: str = self.exporter.export_plan(plan=plan)
        self.assertIn('# Empty trajectory plan', output)

    def test_export_plan_with_waypoints(self) -> None:
        '''
            Verifies exporting populated plan produces valid SCARA script.

            :exceptions: None.
        '''
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
        plan = TrajectoryPlan(waypoints=[wp1, wp2])
        output: str = self.exporter.export_plan(plan=plan)
        self.assertIn('CONFIG ELBOW RIGHT', output)
        self.assertIn('MOVE_J', output)
        self.assertIn('MOVE_L', output)

    def test_export_plan_with_commands_and_moves(self) -> None:
        '''
            Verifies exporting plan preserves non-motion commands in sequence.

            :exceptions: None.
        '''
        waypoints = (
            Waypoint(
                name='START',
                x=10.0,
                y=20.0,
                z=5.0,
                phi=0.0,
                speed=80.0,
                command='',
            ),
            Waypoint(
                name='PUMP_ON',
                x=0.0,
                y=0.0,
                z=0.0,
                phi=0.0,
                speed=0.0,
                command='<CMD:PUMP#1>',
            ),
            Waypoint(
                name='WAIT_500MS',
                x=0.0,
                y=0.0,
                z=0.0,
                phi=0.0,
                speed=0.0,
                command='<CMD:WAIT#500>',
            ),
            Waypoint(
                name='DROP',
                x=30.0,
                y=40.0,
                z=5.0,
                phi=0.0,
                speed=80.0,
                command='',
            ),
            Waypoint(
                name='VALVE_ON',
                x=0.0,
                y=0.0,
                z=0.0,
                phi=0.0,
                speed=0.0,
                command='<CMD:VALVE#1>',
            ),
        )
        plan = TrajectoryPlan(waypoints=waypoints)
        output: str = self.exporter.export_plan(plan=plan)

        self.assertIn('MOVE_J', output)
        self.assertIn('PUMP ON', output)
        self.assertIn('WAIT 500', output)
        self.assertIn('MOVE_L', output)
        self.assertIn('VALVE ON', output)

    def test_get_version(self) -> None:
        '''
            Verifies version reporting.

            :exceptions: None.
        '''
        version: str = self.exporter.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.1.1')


if __name__ == '__main__':
    main()
