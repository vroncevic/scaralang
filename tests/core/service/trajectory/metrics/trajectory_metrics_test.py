# -*- coding: UTF-8 -*-

'''
Module
    trajectory_metrics_test.py
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
    Unit tests for TrajectoryMetrics helper.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.metrics.trajectory_metrics import TrajectoryMetrics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryMetrics(TestCase):
    '''
        Test cases for TrajectoryMetrics mathematical computations.

        It defines:

            :methods:
                | test_distance_between - Verifies 3D Euclidean distance calculation.
                | test_radial_distance - Verifies planar radial reach calculation.
                | test_calculate_distance - Verifies cumulative path distance calculation.
                | test_calculate_duration - Verifies estimated trajectory duration calculation.
    '''

    def test_distance_between(self) -> None:
        '''Verifies 3D distance between two waypoints.'''
        p1 = Waypoint(x=0.0, y=0.0, z=0.0, speed=100.0)
        p2 = Waypoint(x=30.0, y=40.0, z=0.0, speed=100.0)
        dist = TrajectoryMetrics.distance_between(p1, p2)
        self.assertAlmostEqual(dist, 50.0)

    def test_radial_distance(self) -> None:
        '''Verifies planar radial distance calculation.'''
        p = Waypoint(x=60.0, y=80.0, z=10.0, speed=50.0)
        radial = TrajectoryMetrics.radial_distance(p)
        self.assertAlmostEqual(radial, 100.0)

    def test_calculate_distance(self) -> None:
        '''Verifies cumulative path distance calculation.'''
        self.assertEqual(TrajectoryMetrics.calculate_distance([]), 0.0)
        self.assertEqual(
            TrajectoryMetrics.calculate_distance([Waypoint(x=0.0, y=0.0, z=0.0, speed=10.0)]),
            0.0,
        )

        pts = [
            Waypoint(x=0.0, y=0.0, z=0.0, speed=10.0),
            Waypoint(x=10.0, y=0.0, z=0.0, speed=10.0),
            Waypoint(x=10.0, y=20.0, z=0.0, speed=10.0),
        ]
        self.assertAlmostEqual(TrajectoryMetrics.calculate_distance(pts), 30.0)

    def test_calculate_duration(self) -> None:
        '''Verifies estimated execution duration calculation.'''
        self.assertEqual(TrajectoryMetrics.calculate_duration([]), 0.0)

        pts = [
            Waypoint(x=0.0, y=0.0, z=0.0, speed=10.0),
            Waypoint(x=100.0, y=0.0, z=0.0, speed=50.0),
        ]
        # 100 mm at 50 mm/s = 2.0 s
        self.assertAlmostEqual(TrajectoryMetrics.calculate_duration(pts), 2.0)


if __name__ == '__main__':
    main()
