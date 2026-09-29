# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_validator.py
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
    Orchestrates full trajectory plan validation against waypoint and feedrate constraints.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.service.trajectory.metrics.trajectory_metrics import TrajectoryMetrics
from scaralang.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.waypoint.iwaypoint_validator import IWaypointValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryPlanValidator:
    '''
        Orchestrates full trajectory plan validation against waypoint and feedrate constraints.

        It defines:

            :attributes:
                | name - Identifier name of the trajectory plan validator.
                | _waypoint_validator - Injected waypoint reachability validator.
                | _feedrate_validator - Injected feedrate limit validator.
            :methods:
                | __init__ - Initializes plan validator with collaborator validators.
                | validate_plan - Validates entire trajectory plan against kinematic bounds.
    '''

    _waypoint_validator: IWaypointValidator
    _feedrate_validator: IFeedrateValidator

    def __init__(
        self,
        *,
        waypoint_validator: IWaypointValidator,
        feedrate_validator: IFeedrateValidator,
    ) -> None:
        '''
            Initializes trajectory plan validator with injected sub-validators.

            :param waypoint_validator: Injected IWaypointValidator instance.
            :param feedrate_validator: Injected IFeedrateValidator instance.
        '''
        self._waypoint_validator: Final[IWaypointValidator] = waypoint_validator
        self._feedrate_validator: Final[IFeedrateValidator] = feedrate_validator

    @property
    def name(self) -> str:
        '''
            Gets the trajectory plan validator identifier name.

            :return: Validator name string.
        '''
        return 'trajectory_plan_validator'

    def validate_plan(self, plan: ITrajectoryReadOnly) -> tuple[bool, list[str]]:
        '''
            Validates entire trajectory plan against kinematic and feedrate bounds.

            :param plan: ITrajectoryReadOnly instance to validate.
            :return: Tuple of (is_valid, messages_list).
        '''
        waypoints = plan.waypoints

        if not waypoints:
            return False, ['Trajectory plan is empty. Please add waypoints.']

        messages: list[str] = []
        all_valid: bool = True

        for index, pt in enumerate(waypoints, start=1):
            res_pt: ValidationResult = self._waypoint_validator.validate_point(pt)

            if not res_pt.is_valid:
                all_valid = False
                messages.append(
                    f'Point P{index} ({pt.x:.1f}, {pt.y:.1f}, {pt.z:.1f}): {res_pt.message}'
                )

            res_spd: ValidationResult = self._feedrate_validator.validate_feedrate(pt.speed)

            if not res_spd.is_valid:
                all_valid = False
                messages.append(f'Point P{index} Speed ({pt.speed:.1f} mm/s): {res_spd.message}')

        if all_valid:
            total_dist: float = TrajectoryMetrics.calculate_distance(waypoints)
            est_time: float = TrajectoryMetrics.calculate_duration(waypoints)
            messages.append(
                f'Validation PASSED: All {len(waypoints)} waypoints are within reachable '
                f'workspace.\nTotal Path Distance: {total_dist:.2f} mm | '
                f'Estimated Time: {est_time:.2f} s'
            )

        return all_valid, messages
