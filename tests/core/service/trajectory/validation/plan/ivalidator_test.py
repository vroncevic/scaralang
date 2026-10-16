# -*- coding: UTF-8 -*-

'''
Module
    ivalidator_test.py
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
    Unit tests for ITrajectoryPlanValidator protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.validation.feedrate.factory import FeedrateFactory
from scaralang.core.service.trajectory.validation.plan.ivalidator import ITrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.plan.validator import TrajectoryPlanValidator
from scaralang.core.service.trajectory.validation.waypoint.factory import WaypointFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryPlanValidator(TestCase):
    '''
        Test cases verifying ITrajectoryPlanValidator structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies TrajectoryPlanValidator satisfies protocol.
                | test_validator_name - Verifies validator name identifier.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that TrajectoryPlanValidator satisfies ITrajectoryPlanValidator.
        '''
        kinematics = DefaultKinematicsFactory.create()
        wp_val = WaypointFactory.create(workspace=kinematics.workspace).validator
        fr_val = FeedrateFactory.create(bounds=kinematics.envelope.bounds).validator
        validator = TrajectoryPlanValidator(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        self.assertIsInstance(validator, ITrajectoryPlanValidator)

    def test_validator_name(self) -> None:
        '''
            Verifies that validator provides expected name identifier.
        '''
        kinematics = DefaultKinematicsFactory.create()
        wp_val = WaypointFactory.create(workspace=kinematics.workspace).validator
        fr_val = FeedrateFactory.create(bounds=kinematics.envelope.bounds).validator
        validator = TrajectoryPlanValidator(
            waypoint_validator=wp_val,
            feedrate_validator=fr_val,
        )
        self.assertEqual(validator.name, 'trajectory_plan_validator')


if __name__ == '__main__':
    main()
