# -*- coding: UTF-8 -*-

'''
Module
    dead_zone_bypass_planner_factory.py
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
    Factory instantiating DeadZoneBypassPlanner instances.
'''

from __future__ import annotations

from math import pi

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.trajectory.avoidance.dead_zone_bypass_planner import DeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.dead_zone_validator_factory import DeadZoneValidatorFactory
from scaralang.core.service.trajectory.avoidance.idead_zone_bypass_planner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.idead_zone_validator import IDeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneBypassPlannerFactory:
    '''
        Factory providing configured IDeadZoneBypassPlanner instances.

        It defines:

            :methods:
                | create - Builds an IDeadZoneBypassPlanner from validator and margin.
                | create_from_bounds - Builds an IDeadZoneBypassPlanner from ScaraBounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        validator: IDeadZoneValidator,
        safety_margin_mm: float = 5.0,
        angular_step_rad: float = pi / 12.0,
    ) -> IDeadZoneBypassPlanner:
        '''
            Builds and returns an IDeadZoneBypassPlanner instance.

            :param validator: Injected IDeadZoneValidator instance.
            :param safety_margin_mm: Safety clearance margin in mm.
            :param angular_step_rad: Angular arc interpolation resolution in radians.
            :return: Configured IDeadZoneBypassPlanner instance.
            :exceptions: None.
        '''
        return DeadZoneBypassPlanner(
            validator=validator,
            safety_margin_mm=safety_margin_mm,
            angular_step_rad=angular_step_rad,
        )

    @classmethod
    def create_from_bounds(
        cls,
        bounds: ScaraBounds,
        *,
        safety_margin_mm: float = 5.0,
        angular_step_rad: float = pi / 12.0,
    ) -> IDeadZoneBypassPlanner:
        '''
            Builds and returns an IDeadZoneBypassPlanner instance derived from ScaraBounds.

            :param bounds: Injected ScaraBounds kinematic model.
            :param safety_margin_mm: Safety clearance margin in mm.
            :param angular_step_rad: Angular arc interpolation resolution in radians.
            :return: Configured IDeadZoneBypassPlanner instance.
            :exceptions: None.
        '''
        validator: IDeadZoneValidator = DeadZoneValidatorFactory.create_from_bounds(
            bounds=bounds
        )

        return DeadZoneBypassPlanner(
            validator=validator,
            safety_margin_mm=safety_margin_mm,
            angular_step_rad=angular_step_rad,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
