# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for TangentArcCalculator service component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.bypass_arc_geometry import BypassArcGeometry
from scaralang.core.service.trajectory.avoidance.bypass.arc.calculator import TangentArcCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTangentArcCalculator(TestCase):
    '''
        Validates TangentArcCalculator tangential entry, exit, and sweep angle calculations.

        It defines:

            :methods:
                | setUp - Initializes TangentArcCalculator instance.
                | test_calculate_bypass_arc_ccw - Verifies counter-clockwise sweep geometry.
                | test_calculate_bypass_arc_cw - Verifies clockwise sweep geometry.
                | test_calculate_bypass_arc_inside_radius - Verifies fallback when points are within radius.
                | test_get_version - Verifies version string accessor.
    '''

    def setUp(self) -> None:
        '''
            Initializes TangentArcCalculator instance.
        '''
        self.calculator = TangentArcCalculator()

    def test_calculate_bypass_arc_ccw(self) -> None:
        '''
            Verifies CCW bypass arc geometry for crossing segment.
        '''
        p1 = Point2D(x=-120.0, y=10.0)
        p2 = Point2D(x=120.0, y=10.0)
        arc: BypassArcGeometry = self.calculator.calculate_bypass_arc(
            start_pt=p1,
            end_pt=p2,
            safe_radius=85.0,
        )
        self.assertEqual(arc.safe_radius, 85.0)
        self.assertGreater(arc.arc_sweep, 0.0)
        self.assertEqual(arc.step_sign, -1.0)

    def test_calculate_bypass_arc_cw(self) -> None:
        '''
            Verifies CW bypass arc geometry for crossing segment.
        '''
        p1 = Point2D(x=120.0, y=10.0)
        p2 = Point2D(x=-120.0, y=10.0)
        arc: BypassArcGeometry = self.calculator.calculate_bypass_arc(
            start_pt=p1,
            end_pt=p2,
            safe_radius=85.0,
        )
        self.assertEqual(arc.safe_radius, 85.0)
        self.assertGreater(arc.arc_sweep, 0.0)
        self.assertEqual(arc.step_sign, 1.0)

    def test_calculate_bypass_arc_inside_radius(self) -> None:
        '''
            Verifies clamp to zero alpha when points are inside or on safe radius.
        '''
        p1 = Point2D(x=50.0, y=0.0)
        p2 = Point2D(x=0.0, y=50.0)
        arc: BypassArcGeometry = self.calculator.calculate_bypass_arc(
            start_pt=p1,
            end_pt=p2,
            safe_radius=85.0,
        )
        self.assertEqual(arc.safe_radius, 85.0)
        self.assertGreater(arc.arc_sweep, 0.0)

    def test_get_version(self) -> None:
        '''
            Verifies version string accessor returns valid representation.
        '''
        version = self.calculator.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
