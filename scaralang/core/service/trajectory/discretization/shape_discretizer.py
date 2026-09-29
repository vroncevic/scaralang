# -*- coding: UTF-8 -*-

'''
Module
    shape_discretizer.py
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
    Implementation of IShapeDiscretizer discretizing geometric contours into waypoints.
'''

from __future__ import annotations

from math import cos, pi, sin

from scaralang.core.model.trajectory.circle_geometry import CircleGeometry
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapeDiscretizer:
    '''
        Service discretizing 2D geometric CAD shapes into discrete waypoint trajectories.

        It defines:

            :attributes:
                | name - Identifier name of the shape discretizer.
            :methods:
                | __init__ - Initializes ShapeDiscretizer instance.
                | discretize_line - Discretizes straight linear segment.
                | discretize_circle - Discretizes circular boundary into polygonal waypoints.
                | discretize_rectangle - Discretizes rectangular boundary into corner waypoints.
    '''

    def __init__(self) -> None:
        '''
            Initializes ShapeDiscretizer instance.
        '''

    @property
    def name(self) -> str:
        '''
            Gets the shape discretizer identifier name.

            :return: Discretizer name string.
        '''
        return 'shape_discretizer'

    def discretize_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates start and end waypoints of straight linear segment.

            :param p1: Start coordinate (x, y) tuple in mm.
            :param p2: End coordinate (x, y) tuple in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        return [
            Waypoint(x=p1[0], y=p1[1], z=z, speed=speed),
            Waypoint(x=p2[0], y=p2[1], z=z, speed=speed),
        ]

    def discretize_circle(
        self,
        *,
        geometry: CircleGeometry,
    ) -> list[Waypoint]:
        '''
            Generates circle perimeter waypoints.

            :param geometry: CircleGeometry model encapsulating circle parameters.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        pts: list[Waypoint] = []
        center = geometry.center
        radius = geometry.radius
        steps = geometry.steps
        z = geometry.z
        speed = geometry.speed

        for i in range(steps + 1):
            angle: float = 2.0 * pi * (i / steps)
            px: float = center[0] + radius * cos(angle)
            py: float = center[1] + radius * sin(angle)
            pts.append(Waypoint(x=px, y=py, z=z, speed=speed))

        return pts

    def discretize_rectangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates corner waypoints of closed rectangular boundary.

            :param p1: Initial corner coordinate (x, y) tuple in mm.
            :param p2: Opposite corner coordinate (x, y) tuple in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        return [
            Waypoint(x=p1[0], y=p1[1], z=z, speed=speed),
            Waypoint(x=p2[0], y=p1[1], z=z, speed=speed),
            Waypoint(x=p2[0], y=p2[1], z=z, speed=speed),
            Waypoint(x=p1[0], y=p2[1], z=z, speed=speed),
            Waypoint(x=p1[0], y=p1[1], z=z, speed=speed),
        ]
