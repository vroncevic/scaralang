# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines structural protocol IWorkspaceBoundaryService for boundary kinematics calculations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWorkspaceBoundaryService(Protocol):
    '''
        Structural protocol defining workspace unreachable boundary kinematics calculations.

        It defines:

            :methods:
                | is_j1_limited - Checks whether J1 angular range is bounded below PI.
                | calculate_forbidden_zone_polygon - Calculates vertices of rear unreachable zone.
                | get_version - Returns service component version string.
    '''

    def is_j1_limited(self, bounds: ScaraBounds) -> bool:
        '''
            Checks whether J1 angular range is bounded below PI.

            :param bounds: Kinematic geometry and limits model.
            :return: True if J1 is bounded below PI, False otherwise.
        '''

    def calculate_forbidden_zone_polygon(
        self,
        bounds: ScaraBounds,
    ) -> tuple[Point2D, ...]:
        '''
            Calculates the analytical vertices of the rear unreachable boundary crescent.

            :param bounds: Kinematic geometry and limits model.
            :return: Tuple of Point2D Cartesian coordinates in millimeters.
        '''

    def get_version(self) -> str:
        '''
            Returns the service version string.

            :return: Service version string.
        '''
