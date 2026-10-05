# -*- coding: UTF-8 -*-

'''
Module
    ijoint_step_transmission_converter.py
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
    Interface protocol for bidirectional conversion between joint angles and motor steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IJointStepTransmissionConverter(Protocol):
    '''
        Structural interface protocol for joint step transmission conversion.

        It defines:

            :methods:
                | angles_to_steps - Converts joint radians/mm into discrete motor steps.
                | steps_to_angles - Converts discrete motor steps into joint radians/mm.
                | steps_per_rad - Calculates motor step scale factor per radian of joint rotation.
                | steps_per_mm_z - Calculates motor step scale factor per linear mm of Z travel.
    '''

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float
    ) -> tuple[int, int, int, int]:
        '''
            Converts joint angles and linear Z travel into discrete motor steps.

            :param theta1_rad: Shoulder joint angle in radians.
            :param theta2_rad: Elbow joint angle in radians.
            :param z_mm: Linear vertical travel in millimeters.
            :param theta4_rad: Wrist joint angle in radians.
            :return: Tuple of (j1, j2, z, j4) integer microsteps.
        '''

    def steps_to_angles(
        self,
        step1: int,
        step2: int,
        step3: int,
        step4: int
    ) -> tuple[float, float, float, float]:
        '''
            Converts discrete motor steps into joint angles and linear Z travel.

            :param step1: Shoulder joint motor microsteps.
            :param step2: Elbow joint motor microsteps.
            :param step3: Z-axis vertical motor microsteps.
            :param step4: Wrist joint motor microsteps.
            :return: Tuple of (theta1_rad, theta2_rad, z_mm, theta4_rad).
        '''

    def steps_per_rad(self, gear_ratio: float) -> float:
        '''
            Calculates motor step scale factor per radian of joint rotation.

            :param gear_ratio: Mechanical reduction ratio.
            :return: Steps per radian float value.
        '''

    def steps_per_mm_z(self) -> float:
        '''
            Calculates motor step scale factor per linear millimeter of Z travel.

            :return: Steps per millimeter float value.
        '''
