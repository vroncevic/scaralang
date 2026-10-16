# -*- coding: UTF-8 -*-

'''
Module
    service.py
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
    Workspace unreachable boundary kinematics calculation service.
'''

from __future__ import annotations

from math import asin, cos, pi, sin

from typing import ClassVar

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceBoundaryService:
    '''
        Computes analytical geometric boundary vertices for the rear unreachable crescent zone.

        It defines:

            :methods:
                | is_j1_limited - Checks whether J1 angular range is bounded below PI.
                | calculate_forbidden_zone_polygon - Calculates vertices of rear unreachable zone.
                | get_version - Returns service component version string.
    '''

    _STEPS_ARC: ClassVar[int] = 24
    _STEPS_CURVE: ClassVar[int] = 16
    _TWO_PI: ClassVar[float] = 2.0 * pi
    _MAX_SIN: ClassVar[float] = 1.0

    def is_j1_limited(self, bounds: ScaraBounds) -> bool:
        '''
            Checks whether J1 angular range is bounded below PI.

            :param bounds: Kinematic geometry and limits model.
            :return: True if J1 is bounded below PI, False otherwise.
            :exceptions: None.
        '''
        return bounds.joints.j1_max_rad < pi

    def calculate_forbidden_zone_polygon(
        self,
        bounds: ScaraBounds,
    ) -> tuple[Point2D, ...]:
        '''
            Calculates the analytical vertices of the rear unreachable boundary crescent.

            :param bounds: Kinematic geometry and limits model.
            :return: Tuple of Point2D Cartesian coordinates in millimeters.
            :exceptions: None.
        '''
        if not self.is_j1_limited(bounds):
            return ()

        l1: float = bounds.links.l1
        l2: float = bounds.links.l2
        j1_max: float = bounds.joints.j1_max_rad
        r_max: float = l1 + l2

        poly_pts: list[Point2D] = [
            Point2D(
                x=r_max * cos(j1_max + (self._TWO_PI - 2.0 * j1_max) * (i / self._STEPS_ARC)),
                y=r_max * sin(j1_max + (self._TWO_PI - 2.0 * j1_max) * (i / self._STEPS_ARC)),
            )
            for i in range(self._STEPS_ARC + 1)
        ]

        sin_target: float = min(self._MAX_SIN, (l1 * sin(j1_max)) / l2)
        theta2_cross: float = pi - asin(sin_target) - j1_max
        elbow_neg: tuple[float, float] = (l1 * cos(-j1_max), l1 * sin(-j1_max))
        elbow_pos: tuple[float, float] = (l1 * cos(j1_max), l1 * sin(j1_max))

        for i in range(self._STEPS_CURVE + 1):
            arm_ang: float = -j1_max - theta2_cross * (i / self._STEPS_CURVE)
            poly_pts.append(
                Point2D(
                    x=elbow_neg[0] + l2 * cos(arm_ang),
                    y=elbow_neg[1] + l2 * sin(arm_ang),
                )
            )

        for i in range(self._STEPS_CURVE, -1, -1):
            arm_ang = j1_max + theta2_cross * (i / self._STEPS_CURVE)
            poly_pts.append(
                Point2D(
                    x=elbow_pos[0] + l2 * cos(arm_ang),
                    y=elbow_pos[1] + l2 * sin(arm_ang),
                )
            )

        return tuple(poly_pts)

    def get_version(self) -> str:
        '''
            Returns the service version string.

            :return: Service version string.
            :exceptions: None.
        '''
        return __version__
