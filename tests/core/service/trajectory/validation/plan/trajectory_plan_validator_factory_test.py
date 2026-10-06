# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_validator_factory_test.py
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
    Unit tests for TrajectoryPlanValidatorFactory operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.feedrate.feedrate_validator_factory import FeedrateValidatorFactory
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.itrajectory_plan_validator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.waypoint.iwaypoint_validator import IWaypointValidator
from scaralang.core.service.trajectory.validation.plan.trajectory_plan_validator_factory import TrajectoryPlanValidatorFactory
from scaralang.core.service.trajectory.validation.waypoint.waypoint_validator_factory import WaypointValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlanValidatorFactory(TestCase):
    '''
        Test cases verifying TrajectoryPlanValidatorFactory instantiation.

        It defines:

            :methods:
                | test_create_returns_instance - Verifies factory returns ITrajectoryPlanValidator.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_instance(self) -> None:
        '''
            Verifies create builds a valid ITrajectoryPlanValidator instance.
        '''
        kinematics = KinematicsServiceFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        wp_val: IWaypointValidator = WaypointValidatorFactory.create(
            kinematics=kinematics
        )
        fr_val: IFeedrateValidator = FeedrateValidatorFactory.create(
            bounds=kinematics.bounds
        )
        validator = TrajectoryPlanValidatorFactory.create(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        self.assertIsInstance(validator, ITrajectoryPlanValidator)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(TrajectoryPlanValidatorFactory.get_version(), '1.0.6')


if __name__ == '__main__':
    main()
