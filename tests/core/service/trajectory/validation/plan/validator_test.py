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
    Unit tests for TrajectoryPlanValidator trajectory plan validation operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan
from scaralang.core.service.trajectory.validation.feedrate.factory import FeedrateFactory
from scaralang.core.service.trajectory.validation.feedrate.ivalidator import IFeedrateValidator
from scaralang.core.service.trajectory.validation.plan.validator import TrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.waypoint.factory import WaypointFactory
from scaralang.core.service.trajectory.validation.waypoint.ivalidator import IWaypointValidator
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlanValidator(TestCase):
    '''
        Test cases verifying TrajectoryPlanValidator trajectory plan checking.

        It defines:

            :methods:
                | setUp - Prepares test kinematics and TrajectoryPlanValidator instance.
                | test_validate_plan_empty - Verifies empty trajectory plan fails validation.
                | test_validate_plan_valid - Verifies valid trajectory plan passes validation.
                | test_validate_plan_invalid_point - Verifies plan with unreachable point fails.
                | test_validate_plan_invalid_speed - Verifies plan with invalid feedrate fails.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with collaborators and TrajectoryPlanValidator.
        '''
        provides = DefaultKinematicsFactory.create()
        wp_val: IWaypointValidator = WaypointFactory.create(
            workspace=provides.workspace
        ).validator
        fr_val: IFeedrateValidator = FeedrateFactory.create(
            bounds=provides.envelope.bounds
        ).validator
        self.validator = TrajectoryPlanValidator(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )

    def test_validate_plan_empty(self) -> None:
        '''
            Verifies that an empty trajectory plan fails validation.
        '''
        plan: ITrajectoryPlan = TrajectoryPlan()
        is_valid, messages = self.validator.validate_plan(plan)
        self.assertFalse(is_valid)
        self.assertTrue(len(messages) > 0)

    def test_validate_plan_valid(self) -> None:
        '''
            Verifies that a valid trajectory plan passes validation.
        '''
        plan: ITrajectoryPlan = TrajectoryPlan()
        plan.add_point(
            Waypoint(x=150.0, y=100.0, z=0.0, phi=0.0, speed=50.0, name='', command='')
        )
        plan.add_point(
            Waypoint(x=180.0, y=80.0, z=10.0, phi=0.0, speed=40.0, name='', command='')
        )
        is_valid, messages = self.validator.validate_plan(plan)
        self.assertTrue(is_valid)
        self.assertTrue(len(messages) > 0)
        self.assertIn('PASSED', messages[0])

    def test_validate_plan_invalid_point(self) -> None:
        '''
            Verifies that a trajectory plan containing an unreachable point fails.
        '''
        plan: ITrajectoryPlan = TrajectoryPlan()
        plan.add_point(
            Waypoint(x=150.0, y=100.0, z=0.0, phi=0.0, speed=50.0, name='', command='')
        )
        plan.add_point(
            Waypoint(x=900.0, y=900.0, z=0.0, phi=0.0, speed=50.0, name='', command='')
        )
        is_valid, messages = self.validator.validate_plan(plan)
        self.assertFalse(is_valid)
        self.assertTrue(any('reach' in m.lower() or 'workspace' in m.lower() for m in messages))

    def test_validate_plan_invalid_speed(self) -> None:
        '''
            Verifies that a trajectory plan containing an excessive feedrate fails.
        '''
        plan: ITrajectoryPlan = TrajectoryPlan()
        plan.add_point(
            Waypoint(x=150.0, y=100.0, z=0.0, phi=0.0, speed=500.0, name='', command='')
        )
        is_valid, messages = self.validator.validate_plan(plan)
        self.assertFalse(is_valid)
        self.assertTrue(any('exceeds max safe feedrate' in m for m in messages))


if __name__ == '__main__':
    main()
