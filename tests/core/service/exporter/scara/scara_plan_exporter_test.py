# -*- coding: UTF-8 -*-

'''
Module
    scara_plan_exporter_test.py
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
    Unit tests for ScaraPlanExporter class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter
from scaralang.core.service.exporter.scara.scara_plan_exporter import ScaraPlanExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraPlanExporter(TestCase):
    '''
        Test cases verifying ScaraPlanExporter.

        It defines:

            :methods:
                | test_format_waypoint_initial - Verifies initial joint move formatting.
                | test_format_waypoint_linear - Verifies linear move formatting.
                | test_export_plan_empty - Verifies empty plan export output.
                | test_export_plan_with_waypoints - Verifies multi-point export output.
                | test_protocol_conformance - Verifies protocol satisfaction.
    '''

    def setUp(self) -> None:
        '''Sets up ScaraPlanExporter instance.'''
        self.exporter = ScaraPlanExporter()

    def test_format_waypoint_initial(self) -> None:
        '''Verifies format_waypoint generates MOVE_J instruction.'''
        wp = Waypoint(x=10.0, y=20.0, z=5.0, phi=90.0, speed=100.0, name='START')
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=True)
        self.assertEqual(line, 'MOVE_J X=10.00 Y=20.00 Z=5.00 PHI=90.00  # START')

    def test_format_waypoint_linear(self) -> None:
        '''Verifies format_waypoint generates MOVE_L instruction with speed.'''
        wp = Waypoint(x=15.0, y=25.0, z=0.0, phi=0.0, speed=50.0)
        line = self.exporter.format_waypoint(waypoint=wp, is_initial=False)
        self.assertEqual(line, 'MOVE_L X=15.00 Y=25.00 Z=0.00 PHI=0.00 SPEED=50.0')

    def test_export_plan_empty(self) -> None:
        '''Verifies export_plan returns header for empty trajectory plan.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = ()
        output = self.exporter.export_plan(plan=mock_plan)
        self.assertIn('Empty trajectory plan', output)

    def test_export_plan_with_waypoints(self) -> None:
        '''Verifies export_plan generates valid SCARA program for waypoints.'''
        wp1 = Waypoint(x=10.0, y=20.0, z=5.0, phi=90.0, speed=80.0, name='P1')
        wp2 = Waypoint(x=30.0, y=40.0, z=5.0, phi=45.0, speed=80.0, name='P2')
        mock_plan = MagicMock()
        mock_plan.waypoints = (wp1, wp2)

        output = self.exporter.export_plan(plan=mock_plan)
        self.assertIn('CONFIG ELBOW RIGHT', output)
        self.assertIn('SPEED WORK 80.0', output)
        self.assertIn('MOVE_J X=10.00 Y=20.00 Z=5.00 PHI=90.00  # P1', output)
        self.assertIn('MOVE_L X=30.00 Y=40.00 Z=5.00 PHI=45.00 SPEED=80.0  # P2', output)

    def test_protocol_conformance(self) -> None:
        '''Verifies ScaraPlanExporter satisfies IScaraPlanExporter protocol.'''
        self.assertIsInstance(self.exporter, IScaraPlanExporter)


if __name__ == '__main__':
    main()
