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
    Unit test cases for GcodeExporter formatting and serializing.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.exporter.gcode.exporter import GcodeExporter
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGcodeExporter(TestCase):
    '''Test suite validating GcodeExporter serialization logic.'''

    def setUp(self) -> None:
        '''Initializes exporter instance under test.'''
        self.exporter = GcodeExporter()

    def test_format_waypoint_line_rapid(self) -> None:
        '''Verifies formatting a rapid motion waypoint (speed >= 100).'''
        wp = Waypoint(
            name='P_RAPID',
            x=100.0,
            y=200.0,
            z=15.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        line = self.exporter.format_waypoint_line(waypoint=wp)
        self.assertTrue(line.startswith('G0'))
        self.assertIn('X100.000', line)
        self.assertIn('Y200.000', line)
        self.assertIn('Z15.000', line)
        self.assertIn('F6000', line)
        self.assertIn('; P_RAPID', line)

    def test_format_waypoint_line_linear(self) -> None:
        '''Verifies formatting a linear motion waypoint (speed < 100).'''
        wp = Waypoint(
            name='P_WORK',
            x=50.0,
            y=75.0,
            z=5.0,
            phi=0.0,
            speed=50.0,
            command='',
        )
        line = self.exporter.format_waypoint_line(waypoint=wp)
        self.assertTrue(line.startswith('G1'))
        self.assertIn('F3000', line)

    def test_export_gcode(self) -> None:
        '''Verifies exporting full trajectory plan to G-code program.'''
        wp = Waypoint(
            name='START',
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=100.0,
            command='',
        )
        plan = TrajectoryPlan(waypoints=[wp])
        output = self.exporter.export_gcode(plan=plan)
        self.assertIn('G21', output)
        self.assertIn('G90', output)
        self.assertIn('G92 X0 Y0 Z0', output)
        self.assertIn('M2 ; End of program', output)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)


if __name__ == '__main__':
    main()
