# -*- coding: UTF-8 -*-

'''
Module
    trajectory_validator.py
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
    Composite facade enforcing SCARA mechanical reachability and kinematic validation.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.itrajectory_plan_validator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.waypoint.iwaypoint_validator import IWaypointValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryValidator:
    '''
        Enforces SCARA mechanical reachability and kinematic envelope validation.

        It defines:

            :attributes:
                | _kinematics - Injected analytical kinematics service.
                | _waypoint_validator - Injected waypoint reachability validator.
                | _feedrate_validator - Injected feedrate boundary validator.
                | _plan_validator - Injected trajectory plan validator.
            :methods:
                | __init__ - Initializes facade with collaborators.
                | bounds - Returns active bounds model.
                | r_min - Returns inner workspace radius.
                | r_max - Returns outer workspace radius.
                | kinematics - Returns active kinematics service.
                | validate_point - Validates Waypoint coordinates against reachability rules.
                | validate_feedrate - Validates that speed is within safe mechanical range.
                | validate_plan - Validates entire trajectory plan against kinematic bounds.
    '''

    _kinematics: IKinematicsService
    _waypoint_validator: IWaypointValidator
    _feedrate_validator: IFeedrateValidator
    _plan_validator: ITrajectoryPlanValidator

    def __init__(
        self,
        *,
        kinematics: IKinematicsService,
        waypoint_validator: IWaypointValidator,
        feedrate_validator: IFeedrateValidator,
        plan_validator: ITrajectoryPlanValidator,
    ) -> None:
        '''
            Initializes trajectory validator facade using injected collaborators.

            :param kinematics: Injected IKinematicsService instance.
            :param waypoint_validator: Injected IWaypointValidator instance.
            :param feedrate_validator: Injected IFeedrateValidator instance.
            :param plan_validator: Injected ITrajectoryPlanValidator instance.
        '''
        self._kinematics: Final[IKinematicsService] = kinematics
        self._waypoint_validator: Final[IWaypointValidator] = waypoint_validator
        self._feedrate_validator: Final[IFeedrateValidator] = feedrate_validator
        self._plan_validator: Final[ITrajectoryPlanValidator] = plan_validator

    @property
    def bounds(self) -> ScaraBounds:
        '''
            Returns active bounds model.

            :return: ScaraBounds instance.
        '''
        return self._kinematics.bounds

    @property
    def r_min(self) -> float:
        '''
            Returns inner workspace radius (mm).

            :return: Minimum reach radius.
        '''
        return self._kinematics.r_min

    @property
    def r_max(self) -> float:
        '''
            Returns outer workspace radius (mm).

            :return: Maximum reach radius.
        '''
        return self._kinematics.r_max

    @property
    def kinematics(self) -> IKinematicsService:
        '''
            Returns active kinematics service.

            :return: IKinematicsService instance.
        '''
        return self._kinematics

    def validate_point(self, point: Waypoint) -> ValidationResult:
        '''
            Validates Waypoint coordinates against annular reach and vertical bounds.

            :param point: Target Waypoint to validate.
            :return: ValidationResult with pass/fail and descriptive reason.
        '''
        return self._waypoint_validator.validate_point(point)

    def validate_feedrate(self, speed: float) -> ValidationResult:
        '''
            Validates that speed is within safe mechanical operation range.

            :param speed: Feedrate in mm/s.
            :return: ValidationResult with status and details.
        '''
        return self._feedrate_validator.validate_feedrate(speed)

    def validate_plan(self, plan: ITrajectoryReadOnly) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :param plan: ITrajectoryReadOnly instance to validate.
            :return: Tuple of (is_valid, messages_list).
        '''
        return self._plan_validator.validate_plan(plan)
