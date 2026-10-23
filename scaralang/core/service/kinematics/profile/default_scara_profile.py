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

from typing import ClassVar

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scaralang.core.service.kinematics.profile.deadzone.calculator import DeadzoneCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DefaultScaraProfile:
    '''
        Factory providing standard reference robotic kinematics and transmission profiles.

        It defines:

            :attributes:
                | DEFAULT_L1_MM - Default shoulder link length in millimeters.
                | DEFAULT_L2_MM - Default elbow link length in millimeters.
                | DEFAULT_J_LIMIT_RAD - Default joint angle symmetric limit in radians.
                | DEFAULT_Z_MIN_MM - Default minimum vertical limit in millimeters.
                | DEFAULT_Z_MAX_MM - Default maximum vertical limit in millimeters.
                | DEFAULT_MIN_SPEED - Default minimum operational speed in mm/s.
                | DEFAULT_MAX_SPEED - Default maximum operational speed in mm/s.
                | DEFAULT_SPEED - Default nominal operational speed in mm/s.
                | DEFAULT_ACCEL - Default nominal acceleration in mm/s^2.
                | DEFAULT_MAX_ACCEL - Default maximum acceleration in mm/s^2.
                | DEFAULT_SINGULARITY_MARGIN_MM - Default singularity boundary margin in mm.
                | DEFAULT_THETA2_MIN_RAD - Default theta2 singularity margin in radians.
                | DEFAULT_STEPS_PER_REV - Default motor steps per revolution.
                | DEFAULT_MICROSTEPPING - Default microstepping multiplier.
                | DEFAULT_GEAR_RATIO_J1 - Default shoulder joint reduction ratio.
                | DEFAULT_GEAR_RATIO_J2 - Default elbow joint reduction ratio.
                | DEFAULT_GEAR_RATIO_J4 - Default wrist roll joint reduction ratio.
                | DEFAULT_LEADSCREW_PITCH_Z - Default Z-axis leadscrew pitch in mm/rev.
            :methods:
                | calculate_deadzone_radius - Calculates minimum reach dead zone radius.
                | create_bounds - Generates default ScaraBounds domain model.
                | create_dls_config - Generates default DlsConfig numerical IK configuration model.
                | create_transmission - Generates default TransmissionParameters domain model.
                | get_version - Returns profile version string.
    '''

    DEFAULT_L1_MM: ClassVar[float] = 150.0
    DEFAULT_L2_MM: ClassVar[float] = 150.0
    DEFAULT_J_LIMIT_RAD: ClassVar[float] = 2.61799
    DEFAULT_Z_MIN_MM: ClassVar[float] = -50.0
    DEFAULT_Z_MAX_MM: ClassVar[float] = 50.0
    DEFAULT_MIN_SPEED: ClassVar[float] = 1.0
    DEFAULT_MAX_SPEED: ClassVar[float] = 200.0
    DEFAULT_SPEED: ClassVar[float] = 50.0
    DEFAULT_ACCEL: ClassVar[float] = 100.0
    DEFAULT_MAX_ACCEL: ClassVar[float] = 500.0
    DEFAULT_SINGULARITY_MARGIN_MM: ClassVar[float] = 5.0
    DEFAULT_THETA2_MIN_RAD: ClassVar[float] = 0.087266

    DEFAULT_STEPS_PER_REV: ClassVar[float] = 200.0
    DEFAULT_MICROSTEPPING: ClassVar[float] = 16.0
    DEFAULT_GEAR_RATIO_J1: ClassVar[float] = 4.0
    DEFAULT_GEAR_RATIO_J2: ClassVar[float] = 4.0
    DEFAULT_GEAR_RATIO_J4: ClassVar[float] = 1.0
    DEFAULT_LEADSCREW_PITCH_Z: ClassVar[float] = 8.0

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
        return DeadzoneCalculator().calculate_radius(
            l1=l1, l2=l2, j2_max_rad=j2_max_rad
        )

    @classmethod
    def create_bounds(cls) -> ScaraBounds:
        '''
            Builds default robotic workspace and velocity bounds.

            :return: Configured ScaraBounds domain model.
            :exceptions: None.
        '''
        l1: float = cls.DEFAULT_L1_MM
        l2: float = cls.DEFAULT_L2_MM
        j2_max: float = cls.DEFAULT_J_LIMIT_RAD
        deadzone_r_min: float = cls.calculate_deadzone_radius(l1, l2, j2_max)

        return ScaraBounds(
            links=LinkDimensions(l1=l1, l2=l2),
            vertical=VerticalBounds(
                z_min=cls.DEFAULT_Z_MIN_MM, z_max=cls.DEFAULT_Z_MAX_MM
            ),
            speeds=SpeedLimits(
                min_speed=cls.DEFAULT_MIN_SPEED,
                max_speed=cls.DEFAULT_MAX_SPEED,
                default_speed=cls.DEFAULT_SPEED,
                default_accel=cls.DEFAULT_ACCEL,
                max_accel=cls.DEFAULT_MAX_ACCEL,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-cls.DEFAULT_J_LIMIT_RAD,
                j1_max_rad=cls.DEFAULT_J_LIMIT_RAD,
                j2_min_rad=-j2_max,
                j2_max_rad=j2_max,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=cls.DEFAULT_SINGULARITY_MARGIN_MM,
                singularity_inner_margin_mm=cls.DEFAULT_SINGULARITY_MARGIN_MM,
                singularity_theta2_min_rad=cls.DEFAULT_THETA2_MIN_RAD,
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
            steps_per_rev=cls.DEFAULT_STEPS_PER_REV,
            microstepping=cls.DEFAULT_MICROSTEPPING,
            gear_ratio_j1=cls.DEFAULT_GEAR_RATIO_J1,
            gear_ratio_j2=cls.DEFAULT_GEAR_RATIO_J2,
            gear_ratio_j4=cls.DEFAULT_GEAR_RATIO_J4,
            leadscrew_pitch_z=cls.DEFAULT_LEADSCREW_PITCH_Z,
        )

    @classmethod
    def create_dls_config(cls) -> DlsConfig:
        '''
            Builds default Damped Least Squares (DLS) numerical solver configuration.

            :return: Configured DlsConfig domain model.
            :exceptions: None.
        '''
        return DlsConfig()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the profile version string.

            :return: Profile version string.
            :exceptions: None.
        '''
        return __version__
