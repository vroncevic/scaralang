# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for TrajectoryValidator composite facade operations.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.kinematics.iservice import IKinematicsService
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan
from scaralang.core.service.trajectory.validation.feedrate.factory import FeedrateFactory
from scaralang.core.service.trajectory.validation.feedrate.ivalidator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.dependencies import PlanDependencies
from scaralang.core.service.trajectory.validation.plan.factory import PlanFactory
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.validator import TrajectoryValidator
from scaralang.core.service.trajectory.validation.waypoint.factory import WaypointFactory
from scaralang.core.service.trajectory.validation.waypoint.ivalidator import IWaypointValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryValidator(TestCase):
    '''
        Test cases verifying TrajectoryValidator composite facade behavior.

        It defines:

            :methods:
                | setUp - Prepares test fixture with validator and collaborators.
                | test_properties - Verifies kinematic properties exposure.
                | test_validate_point_delegation - Verifies waypoint validation delegation.
                | test_validate_feedrate_delegation - Verifies feedrate validation delegation.
                | test_validate_plan_delegation - Verifies plan validation delegation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with TrajectoryValidator and mock/real sub-validators.
        '''
        self.kinematics: IKinematicsService = (
            DefaultKinematicsFactory.create().service
        )
        wp_val: IWaypointValidator = WaypointFactory.create(
            kinematics=self.kinematics
        ).validator
        fr_val: IFeedrateValidator = FeedrateFactory.create(
            bounds=self.kinematics.bounds
        ).validator
        plan_deps = PlanDependencies(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        plan_val: ITrajectoryPlanValidator = PlanFactory.create(
            dependencies=plan_deps
        ).validator
        self.validator = TrajectoryValidator(
            kinematics=self.kinematics,
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
            plan_validator=plan_val,
        )

    def test_properties(self) -> None:
        '''
            Verifies that TrajectoryValidator exposes kinematic properties correctly.
        '''
        bounds: ScaraBounds = self.validator.bounds
        self.assertEqual(bounds.links.l1, 150.0)
        self.assertEqual(self.validator.r_min, self.kinematics.r_min)
        self.assertEqual(self.validator.r_max, self.kinematics.r_max)
        self.assertEqual(self.validator.kinematics, self.kinematics)

    def test_validate_point_delegation(self) -> None:
        '''
            Verifies that validate_point delegates correctly.
        '''
        wp_valid = Waypoint(x=150.0, y=100.0, z=0.0, speed=50.0)
        res_valid: ValidationResult = self.validator.validate_point(wp_valid)
        self.assertTrue(res_valid.is_valid)

        wp_invalid = Waypoint(x=900.0, y=900.0, z=0.0, speed=50.0)
        res_invalid: ValidationResult = self.validator.validate_point(wp_invalid)
        self.assertFalse(res_invalid.is_valid)

    def test_validate_feedrate_delegation(self) -> None:
        '''
            Verifies that validate_feedrate delegates correctly.
        '''
        res_valid: ValidationResult = self.validator.validate_feedrate(50.0)
        self.assertTrue(res_valid.is_valid)

        res_slow: ValidationResult = self.validator.validate_feedrate(0.1)
        self.assertFalse(res_slow.is_valid)

    def test_validate_plan_delegation(self) -> None:
        '''
            Verifies that validate_plan delegates correctly.
        '''
        plan: ITrajectoryPlan = TrajectoryPlan()
        plan.add_point(Waypoint(x=150.0, y=100.0, z=0.0, speed=50.0))
        is_valid, messages = self.validator.validate_plan(plan)
        self.assertTrue(is_valid)
        self.assertTrue(len(messages) > 0)


if __name__ == '__main__':
    main()
