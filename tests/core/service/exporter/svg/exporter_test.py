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
    Unit test cases for SvgExporter formatting and serializing.
'''

from __future__ import annotations

from unittest import TestCase

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.exporter.svg.exporter import SvgExporter
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSvgExporter(TestCase):
    '''Test suite validating SvgExporter visualization output.'''

    def setUp(self) -> None:
        '''Initializes exporter instance under test.'''
        self.exporter = SvgExporter()

    def test_build_svg_path_empty(self) -> None:
        '''Verifies empty waypoint list results in empty SVG path data.'''
        path_d = self.exporter.build_svg_path(waypoints=[])
        self.assertEqual(path_d, '')

    def test_build_svg_path_connected(self) -> None:
        '''Verifies sequential points translate to Move (M) and Line (L) commands.'''
        wp1 = Waypoint(
            name='P1',
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=50.0,
            command='',
        )
        wp2 = Waypoint(
            name='P2',
            x=100.0,
            y=50.0,
            z=0.0,
            phi=0.0,
            speed=50.0,
            command='',
        )
        path_d = self.exporter.build_svg_path(waypoints=[wp1, wp2])
        self.assertTrue(path_d.startswith('M 400.0 400.0'))
        self.assertIn('L 500.0 350.0', path_d)

    def test_export_svg(self) -> None:
        '''Verifies full XML document creation containing metadata and viewport.'''
        wp = Waypoint(
            name='ORIGIN',
            x=0.0,
            y=0.0,
            z=0.0,
            phi=0.0,
            speed=50.0,
            command='',
        )
        plan = TrajectoryPlan()
        plan.add_point(wp)
        svg_xml = self.exporter.export_svg(plan=plan)
        self.assertIn('<?xml version="1.0" encoding="UTF-8"?>', svg_xml)
        self.assertIn('<svg xmlns="http://www.w3.org/2000/svg"', svg_xml)
        self.assertIn('viewBox="0 0 800 800"', svg_xml)
        self.assertIn('</svg>', svg_xml)

    def test_get_version(self) -> None:
        '''Verifies version reporting.'''
        self.assertIsInstance(self.exporter.get_version(), str)
