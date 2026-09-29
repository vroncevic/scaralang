# -*- coding: UTF-8 -*-

'''
Module
    json_trajectory_exporter_test.py
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
    Unit tests for JsonTrajectoryExporter class.
'''

from __future__ import annotations

from json import loads
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.json.ijson_trajectory_exporter import IJsonTrajectoryExporter
from scaralang.core.service.exporter.json.json_trajectory_exporter import JsonTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJsonTrajectoryExporter(TestCase):
    '''
        Test cases verifying JsonTrajectoryExporter.

        It defines:

            :methods:
                | test_serialize_waypoint - Verifies waypoint dictionary serialization.
                | test_export_json - Verifies complete JSON document generation.
    '''

    def setUp(self) -> None:
        '''Sets up JsonTrajectoryExporter instance.'''
        self.exporter = JsonTrajectoryExporter()

    def test_serialize_waypoint(self) -> None:
        '''Verifies waypoint serialization into dict.'''
        wp = Waypoint(x=100.0, y=50.0, z=10.0, speed=50.0, name='P1')
        data = self.exporter.serialize_waypoint(index=0, waypoint=wp)
        self.assertEqual(data['index'], 0)
        self.assertEqual(data['name'], 'P1')
        self.assertEqual(data['x'], 100.0)

    def test_export_json(self) -> None:
        '''Verifies full plan export into valid JSON string.'''
        mock_plan = MagicMock()
        mock_plan.waypoints = (
            Waypoint(x=50.0, y=50.0, z=0.0, speed=60.0, name='P0'),
        )
        json_text = self.exporter.export_json(plan=mock_plan)
        parsed = loads(json_text)
        self.assertEqual(parsed['waypoint_count'], 1)
        self.assertEqual(len(parsed['waypoints']), 1)
        self.assertEqual(parsed['waypoints'][0]['name'], 'P0')

    def test_protocol_conformance(self) -> None:
        '''Verifies JsonTrajectoryExporter satisfies IJsonTrajectoryExporter.'''
        self.assertIsInstance(self.exporter, IJsonTrajectoryExporter)


if __name__ == '__main__':
    main()
