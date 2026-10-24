# -*- coding: UTF-8 -*-

'''
Module
    rectangle.py
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
    Service discretizing rectangular boundaries into corner waypoints.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.plan.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RectangleDiscretizer:
    '''
        Service discretizing rectangular boundaries into discrete corner waypoints.

        It defines:

            :attributes:
                | NAME - Canonical component identifier name.
                | DEFAULT_PHI - Default orientation angle in degrees.
                | DEFAULT_NAME - Default waypoint identifier label.
                | DEFAULT_COMMAND - Default waypoint command string.
                | name - Identifier name of the rectangle discretizer.
            :methods:
                | discretize - Generates corner waypoints of closed rectangular boundary.
    '''

    NAME: ClassVar[str] = 'rectangle_discretizer'
    DEFAULT_PHI: ClassVar[float] = 0.0
    DEFAULT_NAME: ClassVar[str] = ''
    DEFAULT_COMMAND: ClassVar[str] = ''

    @property
    def name(self) -> str:
        '''
            Gets the rectangle discretizer identifier name.

            :return: Discretizer name string.
        '''
        return self.NAME

    def discretize(
        self,
        p1: Point2D,
        p2: Point2D,
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates corner waypoints of closed rectangular boundary.

            :param p1: Initial corner coordinate Point2D in mm.
            :param p2: Opposite corner coordinate Point2D in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
            :exceptions: None.
        '''
        return [
            Waypoint(
                x=p1.x,
                y=p1.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            ),
            Waypoint(
                x=p2.x,
                y=p1.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            ),
            Waypoint(
                x=p2.x,
                y=p2.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            ),
            Waypoint(
                x=p1.x,
                y=p2.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            ),
            Waypoint(
                x=p1.x,
                y=p1.y,
                z=z,
                phi=self.DEFAULT_PHI,
                speed=speed,
                name=self.DEFAULT_NAME,
                command=self.DEFAULT_COMMAND,
            ),
        ]
