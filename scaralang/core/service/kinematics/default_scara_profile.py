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
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultScaraProfile:
    '''
        Factory providing standard reference robotic kinematics and transmission profiles.

        It defines:

            :methods:
                | create_bounds - Generates default ScaraBounds domain model.
                | create_transmission - Generates default TransmissionParameters domain model.
                | get_version - Returns profile version string.
    '''

    @classmethod
    def create_bounds(cls) -> ScaraBounds:
        '''
            Builds default robotic workspace and velocity bounds.

            :return: Configured ScaraBounds domain model.
            :exceptions: None.
        '''
        return ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=150.0),
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
                j2_min_rad=-2.61799,
                j2_max_rad=2.61799,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=0.087266,
                deadzone_r_min=20.0,
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
            gear_ratio_j2=2.0,
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
