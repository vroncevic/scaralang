# -*- coding: UTF-8 -*-

'''
Module
    arc_interpolator_test.py
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
    Unit tests for ArcInterpolator component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.compiler.arc_geometry import ArcGeometry
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator import ArcInterpolator
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcInterpolator(TestCase):
    '''
        Test cases verifying ArcInterpolator functionality.

        It defines:

            :methods:
                | setUp - Prepares ArcInterpolator test fixture.
                | test_protocol_conformance - Verifies structural IArcInterpolator conformance.
                | test_get_version - Verifies get_version returns valid version string.
                | test_interpolate_zero_radius - Verifies ScaraKinematicsError for zero radius arc.
                | test_interpolate_cw - Verifies clockwise arc segmentation.
                | test_interpolate_ccw - Verifies counter-clockwise arc segmentation.
                | test_interpolate_ccw_wrap_around - Verifies CCW arc when angle_end <= angle_start.
                | test_calculate_point - Verifies public calculate_point coordinate and angle math.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.interpolator = ArcInterpolator()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IArcInterpolator protocol.
        '''
        self.assertIsInstance(self.interpolator, IArcInterpolator)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.interpolator.get_version(), '1.0.5')


    def test_interpolate_zero_radius(self) -> None:
        '''
            Verifies ScaraKinematicsError is raised when offset_i and offset_j are zero.
        '''
        geometry = ArcGeometry(
            start=Point2D(x=10.0, y=10.0),
            target=Point2D(x=10.0, y=10.0),
            offset=Point2D(x=0.0, y=0.0),
            is_clockwise=True,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.interpolator.interpolate(geometry=geometry)

    def test_interpolate_cw(self) -> None:
        '''
            Verifies clockwise circular arc point interpolation.
        '''
        geometry = ArcGeometry(
            start=Point2D(x=100.0, y=0.0),
            target=Point2D(x=0.0, y=100.0),
            offset=Point2D(x=-100.0, y=0.0),
            is_clockwise=True,
            step_angle_deg=10.0,
        )
        points = self.interpolator.interpolate(geometry=geometry)
        self.assertTrue(len(points) >= 4)
        last_pt = points[-1]
        self.assertAlmostEqual(last_pt.point.x, 0.0, places=3)
        self.assertAlmostEqual(last_pt.point.y, 100.0, places=3)

    def test_interpolate_ccw(self) -> None:
        '''
            Verifies counter-clockwise circular arc point interpolation.
        '''
        geometry = ArcGeometry(
            start=Point2D(x=100.0, y=0.0),
            target=Point2D(x=0.0, y=100.0),
            offset=Point2D(x=-100.0, y=0.0),
            is_clockwise=False,
            step_angle_deg=10.0,
        )
        points = self.interpolator.interpolate(geometry=geometry)
        self.assertTrue(len(points) >= 4)
        last_pt = points[-1]
        self.assertAlmostEqual(last_pt.point.x, 0.0, places=3)
        self.assertAlmostEqual(last_pt.point.y, 100.0, places=3)

    def test_calculate_point(self) -> None:
        '''
            Verifies public calculate_point method computes correct Cartesian coordinate.
        '''
        arc_pt = self.interpolator.calculate_point(
            center=Point2D(x=0.0, y=0.0),
            radius=50.0,
            angle=0.0,
            is_clockwise=True,
        )
        self.assertAlmostEqual(arc_pt.point.x, 50.0, places=4)
        self.assertAlmostEqual(arc_pt.point.y, 0.0, places=4)
        self.assertAlmostEqual(arc_pt.heading_deg, -90.0, places=4)

    def test_interpolate_ccw_wrap_around(self) -> None:
        '''
            Verifies CCW arc point interpolation when angle_end <= angle_start.
        '''
        geometry = ArcGeometry(
            start=Point2D(x=0.0, y=100.0),
            target=Point2D(x=100.0, y=0.0),
            offset=Point2D(x=0.0, y=-100.0),
            is_clockwise=False,
            step_angle_deg=10.0,
        )
        points = self.interpolator.interpolate(geometry=geometry)
        self.assertTrue(len(points) >= 4)
        last_pt = points[-1]
        self.assertAlmostEqual(last_pt.point.x, 100.0, places=3)
        self.assertAlmostEqual(last_pt.point.y, 0.0, places=3)


if __name__ == '__main__':
    main()
