# -*- coding: UTF-8 -*-

'''
Module
    arc_geometry_test.py
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
    Unit tests for ArcGeometry data model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcGeometryTest(TestCase):
    '''Unit tests validating ArcGeometry data model attributes and defaults.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify that ArcGeometry holds geometric values correctly.'''
        geom = ArcGeometry(
            start_x=10.0,
            start_y=20.0,
            target_x=30.0,
            target_y=40.0,
            offset_i=5.0,
            offset_j=5.0,
            is_clockwise=True,
            step_angle_deg=2.5,
        )
        self.assertEqual(geom.start_x, 10.0)
        self.assertEqual(geom.start_y, 20.0)
        self.assertEqual(geom.target_x, 30.0)
        self.assertEqual(geom.target_y, 40.0)
        self.assertEqual(geom.offset_i, 5.0)
        self.assertEqual(geom.offset_j, 5.0)
        self.assertTrue(geom.is_clockwise)
        self.assertEqual(geom.step_angle_deg, 2.5)

    def test_default_step_angle(self) -> None:
        '''Verify default step_angle_deg is 5.0 degrees.'''
        geom = ArcGeometry(
            start_x=0.0,
            start_y=0.0,
            target_x=10.0,
            target_y=10.0,
            offset_i=5.0,
            offset_j=0.0,
            is_clockwise=False,
        )
        self.assertEqual(geom.step_angle_deg, 5.0)


if __name__ == '__main__':
    main()
