# -*- coding: UTF-8 -*-

'''
Module
    ihome.py
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
    Defines structural protocol IHomePoseCalculator for reference home pose calculation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.pose.cartesian import CartesianPose

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IHomePoseCalculator(Protocol):
    '''
        Structural protocol defining reference home pose calculation.

        It defines:

            :methods:
                | calculate_home_pose - Calculates the canonical default home Cartesian 4-DOF pose.
                | get_version - Returns calculator component version string.
    '''

    def calculate_home_pose(
        self,
        reach_ratio: float = 0.65,
        z_offset_mm: float = 20.0,
        phi: float = 0.0,
    ) -> CartesianPose:
        '''
            Calculates the canonical default home Cartesian 4-DOF pose.

            :param reach_ratio: Reach multiplier relative to maximum reach.
            :param z_offset_mm: Vertical elevation offset above z_min in mm.
            :param phi: Tool orientation angle in radians.
            :return: CartesianPose instance.
        '''

    def get_version(self) -> str:
        '''
            Returns calculator component version string representation.

            :return: Semantic version string.
        '''
