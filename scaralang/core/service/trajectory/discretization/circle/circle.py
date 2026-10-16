# -*- coding: UTF-8 -*-

'''
Module
    circle.py
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
    Service discretizing circular boundaries into discrete waypoint trajectories.
'''

from __future__ import annotations

from math import cos, pi, sin
from typing import ClassVar

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.trajectory.circle_geometry import CircleGeometry
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CircleDiscretizer:
    '''
        Service discretizing circular boundaries into discrete waypoint trajectories.

        It defines:

            :attributes:
                | NAME - Canonical component identifier name.
                | MIN_STEPS - Minimum allowed discretization steps count.
                | MIN_RADIUS_MM - Minimum circle radius threshold in millimeters.
                | STEP_OFFSET - Loop boundary offset for circular closure.
                | TWO_PI - Full circle radian constant.
                | DEFAULT_PHI - Default orientation angle in degrees.
                | DEFAULT_NAME - Default waypoint identifier label.
                | DEFAULT_COMMAND - Default waypoint command string.
                | name - Identifier name of the circle discretizer.
            :methods:
                | discretize - Discretizes circular boundary into polygonal waypoints.
    '''

    NAME: ClassVar[str] = 'circle_discretizer'
    MIN_STEPS: ClassVar[int] = 1
    MIN_RADIUS_MM: ClassVar[float] = 0.0
    STEP_OFFSET: ClassVar[int] = 1
    TWO_PI: ClassVar[float] = 2.0 * pi
    DEFAULT_PHI: ClassVar[float] = 0.0
    DEFAULT_NAME: ClassVar[str] = ''
    DEFAULT_COMMAND: ClassVar[str] = ''

    @property
    def name(self) -> str:
        '''
            Gets the circle discretizer identifier name.

            :return: Discretizer name string.
        '''
        return self.NAME

    def discretize(
        self,
        *,
        geometry: CircleGeometry,
    ) -> list[Waypoint]:
        '''
            Generates circle perimeter waypoints.

            :param geometry: CircleGeometry model encapsulating circle parameters.
            :return: List of Waypoint instances.
            :exceptions: ScaraKinematicsError if steps <= 0 or radius <= 0.
        '''
        if geometry.steps < self.MIN_STEPS:
            raise ScaraKinematicsError(
                f'Circle discretization steps must be greater than zero, got {geometry.steps}'
            )

        if geometry.radius <= self.MIN_RADIUS_MM:
            raise ScaraKinematicsError(
                f'Circle radius must be greater than zero, got {geometry.radius}'
            )

        pts: list[Waypoint] = []
        center = geometry.center
        radius = geometry.radius
        steps = geometry.steps
        z = geometry.z
        speed = geometry.speed

        for i in range(steps + self.STEP_OFFSET):
            angle: float = self.TWO_PI * (i / steps)
            px: float = center.x + radius * cos(angle)
            py: float = center.y + radius * sin(angle)
            pts.append(
                Waypoint(
                    x=px,
                    y=py,
                    z=z,
                    phi=self.DEFAULT_PHI,
                    speed=speed,
                    name=self.DEFAULT_NAME,
                    command=self.DEFAULT_COMMAND,
                )
            )

        return pts
