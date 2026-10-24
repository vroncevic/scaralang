# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory constructing kinematics bounds and transmission parameters from dictionary data.
'''

from __future__ import annotations

from collections.abc import Mapping

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProfileFactory:
    '''
        Factory constructing kinematics bounds and transmission parameters from dictionary data.

        It defines:

            :methods:
                | create_bounds_from_dict - Builds ScaraBounds from dictionary mapping.
                | create_transmission_from_dict - Builds TransmissionParameters from dictionary.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_bounds_from_dict(
        cls,
        data: Mapping[str, object],
    ) -> ScaraBounds:
        '''
            Builds ScaraBounds domain model from raw configuration dictionary mapping.

            :param data: Dictionary mapping containing kinematic parameters.
            :return: Configured ScaraBounds domain model.
            :exceptions: None.
        '''
        defaults: ScaraBounds = DefaultScaraProfile.create_bounds()
        l1: float = float(data.get('l1', defaults.links.l1))
        l2: float = float(data.get('l2', defaults.links.l2))
        j2_max: float = float(
            data.get('j2_max_rad', data.get('j2_max', defaults.joints.j2_max_rad))
        )
        deadzone_val: object = data.get('deadzone_r_min')
        deadzone_r_min: float = (
            float(deadzone_val)
            if deadzone_val is not None and float(deadzone_val) > 0.0
            else DefaultScaraProfile.calculate_deadzone_radius(l1, l2, j2_max)
        )

        return ScaraBounds(
            links=LinkDimensions(l1=l1, l2=l2),
            vertical=VerticalBounds(
                z_min=float(data.get('z_min', defaults.vertical.z_min)),
                z_max=float(data.get('z_max', defaults.vertical.z_max)),
            ),
            speeds=SpeedLimits(
                min_speed=float(data.get('min_speed', defaults.speeds.min_speed)),
                max_speed=float(data.get('max_speed', defaults.speeds.max_speed)),
                default_speed=float(data.get('default_speed', defaults.speeds.default_speed)),
                default_accel=float(data.get('default_accel', defaults.speeds.default_accel)),
                max_accel=float(data.get('max_accel', defaults.speeds.max_accel)),
            ),
            joints=JointAngleBounds(
                j1_min_rad=float(
                    data.get('j1_min_rad', data.get('j1_min', defaults.joints.j1_min_rad))
                ),
                j1_max_rad=float(
                    data.get('j1_max_rad', data.get('j1_max', defaults.joints.j1_max_rad))
                ),
                j2_min_rad=float(
                    data.get('j2_min_rad', data.get('j2_min', defaults.joints.j2_min_rad))
                ),
                j2_max_rad=j2_max,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=float(
                    data.get(
                        'singularity_outer_margin_mm',
                        defaults.singularity.singularity_outer_margin_mm,
                    )
                ),
                singularity_inner_margin_mm=float(
                    data.get(
                        'singularity_inner_margin_mm',
                        defaults.singularity.singularity_inner_margin_mm,
                    )
                ),
                singularity_theta2_min_rad=float(
                    data.get(
                        'singularity_theta2_min_rad',
                        defaults.singularity.singularity_theta2_min_rad,
                    )
                ),
                deadzone_r_min=deadzone_r_min,
            ),
        )

    @classmethod
    def create_transmission_from_dict(
        cls,
        data: Mapping[str, object],
    ) -> TransmissionParameters:
        '''
            Builds TransmissionParameters model from raw configuration dictionary mapping.

            :param data: Dictionary mapping containing transmission parameters.
            :return: Configured TransmissionParameters domain model.
            :exceptions: None.
        '''
        defaults: TransmissionParameters = DefaultScaraProfile.create_transmission()

        return TransmissionParameters(
            steps_per_rev=float(data.get('steps_per_rev', defaults.steps_per_rev)),
            microstepping=float(data.get('microstepping', defaults.microstepping)),
            gear_ratio_j1=float(data.get('gear_ratio_j1', defaults.gear_ratio_j1)),
            gear_ratio_j2=float(data.get('gear_ratio_j2', defaults.gear_ratio_j2)),
            gear_ratio_j4=float(data.get('gear_ratio_j4', defaults.gear_ratio_j4)),
            leadscrew_pitch_z=float(data.get('leadscrew_pitch_z', defaults.leadscrew_pitch_z)),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
