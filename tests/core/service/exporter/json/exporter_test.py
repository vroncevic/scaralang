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
    Unit test cases for JsonExporter formatting and serializing.
'''

from __future__ import annotations

from json import loads
from unittest import TestCase

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.json.exporter import JsonExporter
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJsonExporter(TestCase):
    '''Test suite validating JsonExporter serialization logic.'''

    def setUp(self) -> None:
        '''Initializes exporter instance under test.'''
        self.exporter = JsonExporter()

    def test_serialize_waypoint(self) -> None:
        '''Verifies converting a single Waypoint into JSON-serializable dictionary.'''
        wp = Waypoint(
            name='TEST_WP',
            x=12.3456,
            y=23.4567,
            z=34.5678,
            phi=45.6789,
            speed=75.0,
            command='MOVE_L',
        )
        d = self.exporter.serialize_waypoint(index=5, waypoint=wp)
        self.assertEqual(d['index'], 5)
        self.assertEqual(d['name'], 'TEST_WP')
        self.assertEqual(d['x'], 12.346)
        self.assertEqual(d['y'], 23.457)
        self.assertEqual(d['z'], 34.568)
        self.assertEqual(d['phi'], 45.679)
        self.assertEqual(d['speed'], 75.0)
        self.assertEqual(d['command'], 'MOVE_L')

    def test_export_json_valid_plan(self) -> None:
        '''Verifies serializing a trajectory plan into valid JSON string.'''
        wp = Waypoint(name='P1', x=10.0, y=20.0, z=30.0, phi=40.0, speed=50.0)
        plan = TrajectoryPlan()
        plan.add_point(wp)
        json_str = self.exporter.export_json(plan=plan)
        parsed = loads(json_str)
        self.assertEqual(parsed['waypoint_count'], 1)
        self.assertEqual(len(parsed['waypoints']), 1)
        self.assertEqual(parsed['waypoints'][0]['name'], 'P1')

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)
