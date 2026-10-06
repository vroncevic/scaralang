# -*- coding: UTF-8 -*-

'''
Module
    csv_trajectory_exporter_test.py
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
    Unit tests for CsvTrajectoryExporter class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.csv.csv_trajectory_exporter import CsvTrajectoryExporter
from scaralang.core.service.exporter.csv.icsv_trajectory_exporter import ICsvTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCsvTrajectoryExporter(TestCase):
    '''
        Test cases verifying CsvTrajectoryExporter.

        It defines:

            :methods:
                | test_format_row - Verifies CSV row formatting.
                | test_export_csv - Verifies complete CSV document generation.
    '''

    def setUp(self) -> None:
        '''Sets up CsvTrajectoryExporter instance.'''
        self.exporter = CsvTrajectoryExporter()

    def test_format_row(self) -> None:
        '''Verifies waypoint formatting into comma-separated row.'''
        wp = Waypoint(x=100.0, y=50.0, z=10.0, speed=50.0, name='P1')
        row = self.exporter.format_row(index=0, waypoint=wp)
        self.assertEqual(row, '0,P1,100.000,50.000,10.000,0.000,50.0,')

    def test_export_csv(self) -> None:
        '''Verifies full plan export into CSV lines.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = (
            Waypoint(x=50.0, y=50.0, z=0.0, speed=60.0, name='P0'),
        )
        csv_text = self.exporter.export_csv(plan=mock_plan)
        self.assertIn('index,name,x_mm,y_mm,z_mm,phi_deg,speed_pct,command', csv_text)
        self.assertIn('0,P0,50.000,50.000,0.000,0.000,60.0,', csv_text)

    def test_protocol_conformance(self) -> None:
        '''Verifies CsvTrajectoryExporter satisfies ICsvTrajectoryExporter.'''
        self.assertIsInstance(self.exporter, ICsvTrajectoryExporter)


if __name__ == '__main__':
    main()
