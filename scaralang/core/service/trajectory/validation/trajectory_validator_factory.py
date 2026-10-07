# -*- coding: UTF-8 -*-

'''
Module
    trajectory_validator_factory.py
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
    Factory instantiating and wiring TrajectoryValidator component with sub-validators.
'''

from __future__ import annotations

from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.trajectory.validation.feedrate.feedrate_validator_factory import FeedrateValidatorFactory
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.itrajectory_plan_validator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scaralang.core.service.trajectory.validation.waypoint.iwaypoint_validator import IWaypointValidator
from scaralang.core.service.trajectory.validation.plan.trajectory_plan_validator_factory import TrajectoryPlanValidatorFactory
from scaralang.core.service.trajectory.validation.trajectory_validator import TrajectoryValidator
from scaralang.core.service.trajectory.validation.waypoint.waypoint_validator_factory import WaypointValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryValidatorFactory:
    '''
        Factory instantiating and wiring TrajectoryValidator component with collaborators.

        It defines:

            :methods:
                | create - Builds TrajectoryValidator instance with injected kinematics.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, kinematics: IKinematicsService) -> ITrajectoryValidator:
        '''
            Builds TrajectoryValidator instance with injected kinematics and sub-validators.

            :param kinematics: Injected IKinematicsService instance.
            :return: ITrajectoryValidator structural protocol instance.
            :exceptions: None.
        '''
        waypoint_val: IWaypointValidator = WaypointValidatorFactory.create(
            kinematics=kinematics
        )
        feedrate_val: IFeedrateValidator = FeedrateValidatorFactory.create(
            bounds=kinematics.bounds
        )
        plan_val: ITrajectoryPlanValidator = TrajectoryPlanValidatorFactory.create(
            waypoint_validator=waypoint_val,
            feedrate_validator=feedrate_val,
        )

        return TrajectoryValidator(
            kinematics=kinematics,
            waypoint_validator=waypoint_val,
            feedrate_validator=feedrate_val,
            plan_validator=plan_val,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
