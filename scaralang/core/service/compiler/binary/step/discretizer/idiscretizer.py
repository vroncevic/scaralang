# -*- coding: UTF-8 -*-

'''
Module
    idiscretizer.py
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
    Defines IStepDiscretizer Protocol for converting Cartesian waypoints to joint steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.kinematics.joint_angles import JointAngles
from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStepDiscretizer(Protocol):
    '''
        Structural protocol defining joint step discretization.

        It defines:

            :methods:
                | angles_to_steps - Converts joint radians/mm to integer motor steps.
                | discretize_waypoint - Solves IK and maps Cartesian waypoint into JointSteps.
                | get_version - Returns implementation version string.
    '''

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float,
    ) -> JointStepCoordinates:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: JointStepCoordinates containing (j1, j2, z, j4) integer microsteps.
        '''

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: JointAngles,
    ) -> tuple[JointSteps, JointAngles]:
        '''
            Solves IK and converts Cartesian waypoint into motor steps with duration.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Preceding joint angles model.
            :return: Tuple of (JointSteps model, new joint angles model).
        '''

    def get_version(self) -> str:
        '''
            Returns implementation version string.

            :return: Version string.
        '''
