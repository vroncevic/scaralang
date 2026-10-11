# -*- coding: UTF-8 -*-

'''
Module
    default_scara_profile.py
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
    Provides default robotic kinematics and transmission parameter profiles.
'''

from __future__ import annotations

from math import cos, pi, sqrt

from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds
from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.singularity_margins import SingularityMargins
from scaralang.core.model.kinematics.speed_limits import SpeedLimits
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.model.kinematics.vertical_bounds import VerticalBounds

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultScaraProfile:
    '''
        Factory providing standard reference robotic kinematics and transmission profiles.

        It defines:

            :methods:
                | calculate_deadzone_radius - Calculates minimum reach dead zone radius.
                | create_bounds - Generates default ScaraBounds domain model.
                | create_transmission - Generates default TransmissionParameters domain model.
                | get_version - Returns profile version string.
    '''

    @classmethod
    def calculate_deadzone_radius(
        cls,
        l1: float,
        l2: float,
        j2_max_rad: float,
    ) -> float:
        '''
            Calculates the physical minimum reach dead zone radius.

            :param l1: Shoulder link length in mm.
            :param l2: Elbow link length in mm.
            :param j2_max_rad: Maximum elbow joint angle in radians.
            :return: Dead zone radius in mm.
            :exceptions: None.
        '''
        return max(
            abs(l1 - l2),
            sqrt(l1**2 + l2**2 - 2.0 * l1 * l2 * cos(pi - abs(j2_max_rad))),
        )

    @classmethod
    def create_bounds(cls) -> ScaraBounds:
        '''
            Builds default robotic workspace and velocity bounds.

            :return: Configured ScaraBounds domain model.
            :exceptions: None.
        '''
        l1: float = 150.0
        l2: float = 150.0
        j2_max: float = 2.61799
        deadzone_r_min: float = cls.calculate_deadzone_radius(l1, l2, j2_max)

        return ScaraBounds(
            links=LinkDimensions(l1=l1, l2=l2),
            vertical=VerticalBounds(z_min=-50.0, z_max=50.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=200.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-2.61799,
                j1_max_rad=2.61799,
                j2_min_rad=-j2_max,
                j2_max_rad=j2_max,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=0.087266,
                deadzone_r_min=deadzone_r_min,
            ),
        )

    @classmethod
    def create_transmission(cls) -> TransmissionParameters:
        '''
            Builds default motor transmission parameters.

            :return: Configured TransmissionParameters domain model.
            :exceptions: None.
        '''
        return TransmissionParameters(
            steps_per_rev=200.0,
            microstepping=16.0,
            gear_ratio_j1=4.0,
            gear_ratio_j2=4.0,
            gear_ratio_j4=1.0,
            leadscrew_pitch_z=8.0,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the profile version string.

            :return: Profile version string.
            :exceptions: None.
        '''
        return __version__
