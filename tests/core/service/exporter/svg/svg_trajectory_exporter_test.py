# -*- coding: UTF-8 -*-

'''
Module
    svg_trajectory_exporter_test.py
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
    Unit tests for SvgTrajectoryExporter class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.svg.isvg_trajectory_exporter import ISvgTrajectoryExporter
from scaralang.core.service.exporter.svg.svg_trajectory_exporter import SvgTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSvgTrajectoryExporter(TestCase):
    '''
        Test cases verifying SvgTrajectoryExporter.

        It defines:

            :methods:
                | test_build_svg_path - Verifies path segment construction.
                | test_export_svg - Verifies complete SVG document generation.
    '''

    def setUp(self) -> None:
        '''Sets up SvgTrajectoryExporter instance.'''
        self.exporter = SvgTrajectoryExporter()

    def test_build_svg_path(self) -> None:
        '''Verifies path generation with Move and Line commands.'''
        wp1 = Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)
        wp2 = Waypoint(x=30.0, y=40.0, z=0.0, speed=50.0)
        cmd_wp = Waypoint(x=0.0, y=0.0, z=0.0, speed=0.0, command='PUMP ON')

        path_d = self.exporter.build_svg_path(waypoints=(wp1, cmd_wp, wp2))
        self.assertEqual(path_d, 'M 10.00 20.00 L 30.00 40.00')

    def test_export_svg(self) -> None:
        '''Verifies full plan export into valid SVG XML string.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = (
            Waypoint(x=50.0, y=50.0, z=0.0, speed=60.0),
        )
        svg_text = self.exporter.export_svg(plan=mock_plan)
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', svg_text)
        self.assertIn('<path d="M 50.00 50.00"', svg_text)
        self.assertIn('</svg>', svg_text)

    def test_protocol_conformance(self) -> None:
        '''Verifies SvgTrajectoryExporter satisfies ISvgTrajectoryExporter.'''
        self.assertIsInstance(self.exporter, ISvgTrajectoryExporter)


if __name__ == '__main__':
    main()
