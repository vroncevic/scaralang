# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_validator_test.py
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
    Unit tests for DeadZoneValidator service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.trajectory.avoidance.dead_zone_validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadZoneValidator(TestCase):
    '''
        Test cases for DeadZoneValidator point and segment boundary checking.

        It defines:

            :methods:
                | setUp - Initializes DeadZoneValidator with standard threshold.
                | test_is_point_in_dead_zone_inside - Verifies detection of points inside dead zone.
                | test_is_point_in_dead_zone_outside - Verifies detection of points outside dead zone.
                | test_is_segment_crossing_origin_cut - Verifies detection of segment cutting across center.
                | test_is_segment_crossing_start_inside - Verifies segment with start inside is flagged.
                | test_is_segment_crossing_end_inside - Verifies segment with end inside is flagged.
                | test_is_segment_crossing_outside - Verifies safe segment outside dead zone returns False.
                | test_is_segment_crossing_zero_length - Verifies degenerate zero-length segments.
                | test_get_dead_zone_radius - Verifies radius accessor returns configured threshold.
                | test_negative_radius_clamped - Verifies negative radius parameter clamps to zero.
                | test_get_version - Verifies version string accessor returns valid representation.
    '''

    def setUp(self) -> None:
        '''Initializes DeadZoneValidator instance with 86.0 mm radius.'''
        self.validator = DeadZoneValidator(dead_zone_radius=86.0)

    def test_is_point_in_dead_zone_inside(self) -> None:
        '''Verifies points strictly inside dead zone return True.'''
        self.assertTrue(self.validator.is_point_in_dead_zone(0.0, 0.0))
        self.assertTrue(self.validator.is_point_in_dead_zone(50.0, 50.0))
        self.assertTrue(self.validator.is_point_in_dead_zone(-80.0, 0.0))

    def test_is_point_in_dead_zone_outside(self) -> None:
        '''Verifies points outside or on boundary return False.'''
        self.assertFalse(self.validator.is_point_in_dead_zone(86.0, 0.0))
        self.assertFalse(self.validator.is_point_in_dead_zone(120.0, 100.0))
        self.assertFalse(self.validator.is_point_in_dead_zone(-150.0, -150.0))

    def test_is_segment_crossing_origin_cut(self) -> None:
        '''Verifies linear segment crossing through center returns True.'''
        p1 = Point2D(x=-120.0, y=0.0)
        p2 = Point2D(x=120.0, y=0.0)
        self.assertTrue(self.validator.is_segment_crossing_dead_zone(p1, p2))

    def test_is_segment_crossing_start_inside(self) -> None:
        '''Verifies segment starting inside dead zone returns True.'''
        p1 = Point2D(x=20.0, y=20.0)
        p2 = Point2D(x=150.0, y=100.0)
        self.assertTrue(self.validator.is_segment_crossing_dead_zone(p1, p2))

    def test_is_segment_crossing_end_inside(self) -> None:
        '''Verifies segment ending inside dead zone returns True.'''
        p1 = Point2D(x=150.0, y=100.0)
        p2 = Point2D(x=-30.0, y=10.0)
        self.assertTrue(self.validator.is_segment_crossing_dead_zone(p1, p2))

    def test_is_segment_crossing_outside(self) -> None:
        '''Verifies segment remaining fully outside dead zone returns False.'''
        p1 = Point2D(x=120.0, y=120.0)
        p2 = Point2D(x=160.0, y=120.0)
        self.assertFalse(self.validator.is_segment_crossing_dead_zone(p1, p2))

    def test_is_segment_crossing_zero_length(self) -> None:
        '''Verifies degenerate zero-length segment behavior.'''
        inside_pt = Point2D(x=10.0, y=10.0)
        outside_pt = Point2D(x=150.0, y=150.0)
        self.assertTrue(self.validator.is_segment_crossing_dead_zone(inside_pt, inside_pt))
        self.assertFalse(self.validator.is_segment_crossing_dead_zone(outside_pt, outside_pt))

    def test_get_dead_zone_radius(self) -> None:
        '''Verifies radius getter matches configured value.'''
        self.assertEqual(self.validator.get_dead_zone_radius(), 86.0)

    def test_negative_radius_clamped(self) -> None:
        '''Verifies negative radius clamps to 0.0.'''
        neg_validator = DeadZoneValidator(dead_zone_radius=-10.0)
        self.assertEqual(neg_validator.get_dead_zone_radius(), 0.0)

    def test_get_version(self) -> None:
        '''Verifies version string is valid.'''
        self.assertIsInstance(self.validator.get_version(), str)
        self.assertTrue(len(self.validator.get_version()) > 0)


if __name__ == '__main__':
    main()
