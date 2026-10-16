# -*- coding: UTF-8 -*-

'''
Module
    service_test.py
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
    Unit tests for WorkspaceBoundaryService calculation component.
'''

from __future__ import annotations

from math import pi
from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.profile.factory import ProfileFactory
from scaralang.core.service.kinematics.workspace.boundary.service import WorkspaceBoundaryService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceBoundaryService(TestCase):
    '''
        Test cases verifying WorkspaceBoundaryService methods.

        It defines:

            :methods:
                | test_is_j1_limited_true - Verifies J1 limited check when j1_max < pi.
                | test_is_j1_limited_false - Verifies J1 limited check when j1_max >= pi.
                | test_calculate_forbidden_zone_unlimited - Verifies empty polygon when unlimited.
                | test_calculate_forbidden_zone_limited - Verifies polygon vertices when limited.
                | test_get_version - Verifies component version string.
    '''

    def test_is_j1_limited_true(self) -> None:
        '''
            Verifies J1 limited check returns True when j1_max < pi.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        service = WorkspaceBoundaryService()
        self.assertTrue(service.is_j1_limited(bounds))

    def test_is_j1_limited_false(self) -> None:
        '''
            Verifies J1 limited check returns False when j1_max >= pi.
        '''
        bounds: ScaraBounds = ProfileFactory.create_bounds_from_dict({
            'j1_min_rad': -pi,
            'j1_max_rad': pi,
        })
        service = WorkspaceBoundaryService()
        self.assertFalse(service.is_j1_limited(bounds))

    def test_calculate_forbidden_zone_unlimited(self) -> None:
        '''
            Verifies empty polygon is returned when J1 is not limited below PI.
        '''
        bounds: ScaraBounds = ProfileFactory.create_bounds_from_dict({
            'j1_min_rad': -pi,
            'j1_max_rad': pi,
        })
        service = WorkspaceBoundaryService()
        poly: tuple[Point2D, ...] = service.calculate_forbidden_zone_polygon(bounds)
        self.assertEqual(len(poly), 0)

    def test_calculate_forbidden_zone_limited(self) -> None:
        '''
            Verifies non-empty polygon vertices are returned when J1 is limited.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        service = WorkspaceBoundaryService()
        poly: tuple[Point2D, ...] = service.calculate_forbidden_zone_polygon(bounds)
        self.assertTrue(len(poly) > 0)
        self.assertTrue(all(isinstance(pt, Point2D) for pt in poly))
        min_x: float = min(pt.x for pt in poly)
        self.assertTrue(min_x < -100.0)

    def test_get_version(self) -> None:
        '''
            Verifies service version string.
        '''
        service = WorkspaceBoundaryService()
        version: str = service.get_version()
        self.assertTrue(isinstance(version, str))
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
