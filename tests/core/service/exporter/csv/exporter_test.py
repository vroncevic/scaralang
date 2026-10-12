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
    Unit test cases for CsvExporter formatting and serializing.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.csv.exporter import CsvExporter
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCsvExporter(TestCase):
    '''Test suite validating CsvExporter serialization logic.'''

    def setUp(self) -> None:
        '''Initializes exporter instance under test.'''
        self.exporter = CsvExporter()

    def test_format_row(self) -> None:
        '''Verifies formatting a single waypoint into a CSV row.'''
        wp = Waypoint(
            name='P1',
            x=150.0,
            y=100.0,
            z=25.0,
            phi=45.0,
            speed=80.0,
            command='MOVE_L',
        )
        row = self.exporter.format_row(index=0, waypoint=wp)
        self.assertEqual(row, '0,P1,150.000,100.000,25.000,45.000,80.0,MOVE_L')

    def test_export_csv_empty_plan(self) -> None:
        '''Verifies exporting an empty plan yields only the CSV header.'''
        plan = TrajectoryPlan()
        output = self.exporter.export_csv(plan=plan)
        expected = 'index,name,x_mm,y_mm,z_mm,phi_deg,speed_pct,command\n'
        self.assertEqual(output, expected)

    def test_export_csv_multiple_waypoints(self) -> None:
        '''Verifies exporting a plan with multiple waypoints.'''
        wp1 = Waypoint(name='P1', x=100.0, y=50.0, z=10.0, phi=0.0, speed=50.0)
        wp2 = Waypoint(name='P2', x=200.0, y=75.0, z=20.0, phi=30.0, speed=60.0)
        plan = TrajectoryPlan()
        plan.add_point(wp1)
        plan.add_point(wp2)
        output = self.exporter.export_csv(plan=plan)
        lines = output.strip().split('\n')
        self.assertEqual(len(lines), 3)
        self.assertIn('P1', lines[1])
        self.assertIn('P2', lines[2])

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)
