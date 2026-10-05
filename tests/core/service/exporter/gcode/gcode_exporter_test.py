# -*- coding: UTF-8 -*-

'''
Module
    gcode_exporter_test.py
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
    Unit tests for GCodeExporter class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.gcode.gcode_exporter import GCodeExporter
from scaralang.core.service.exporter.gcode.igcode_exporter import IGCodeExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestGCodeExporter(TestCase):
    '''
        Test cases verifying GCodeExporter.

        It defines:

            :methods:
                | test_format_waypoint_line - Verifies G-code line formatting.
                | test_export_gcode - Verifies complete G-code program generation.
    '''

    def setUp(self) -> None:
        '''Sets up GCodeExporter instance.'''
        self.exporter = GCodeExporter()

    def test_format_waypoint_line(self) -> None:
        '''Verifies linear and rapid move line formatting.'''
        linear_wp = Waypoint(x=100.0, y=50.0, z=10.0, speed=50.0)
        rapid_wp = Waypoint(x=150.0, y=75.0, z=20.0, speed=100.0)
        cmd_wp = Waypoint(x=0.0, y=0.0, z=0.0, speed=0.0, command='PUMP ON')

        self.assertIn('G01', self.exporter.format_waypoint_line(waypoint=linear_wp))
        self.assertIn('G00', self.exporter.format_waypoint_line(waypoint=rapid_wp))
        self.assertIn('CMD: PUMP ON', self.exporter.format_waypoint_line(waypoint=cmd_wp))

    def test_export_gcode(self) -> None:
        '''Verifies full plan export.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = (
            Waypoint(x=50.0, y=50.0, z=0.0, speed=60.0),
        )
        gcode = self.exporter.export_gcode(plan=mock_plan)
        self.assertIn('G21', gcode)
        self.assertIn('G90', gcode)
        self.assertIn('M30', gcode)
        self.assertIn('X50.000', gcode)

    def test_protocol_conformance(self) -> None:
        '''Verifies GCodeExporter satisfies IGCodeExporter.'''
        self.assertIsInstance(self.exporter, IGCodeExporter)


if __name__ == '__main__':
    main()
