# -*- coding: UTF-8 -*-

'''
Module
    waypoint_validator_test.py
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
    Unit tests for WaypointValidator reachability checking operations.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.waypoint.waypoint_validator import WaypointValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointValidator(TestCase):
    '''
        Test cases verifying WaypointValidator reachability checking.

        It defines:

            :methods:
                | setUp - Prepares test kinematics and validator instance.
                | test_validator_name - Verifies validator name property.
                | test_validate_point_valid - Verifies valid reachable waypoint passes.
                | test_validate_point_out_of_workspace_z - Verifies Z limit violation is detected.
                | test_validate_point_unreachable - Verifies distant unreachable point fails.
                | test_validate_point_violates_joint_limits - Verifies point violating joint limits fails.
                | test_validate_point_kinematically_unreachable - Verifies mathematical reach failure.
                | test_validate_point_empty_reasons - Verifies fallback message when reasons is empty.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with KinematicsService and WaypointValidator.
        '''
        kinematics: IKinematicsService = KinematicsServiceFactory.create(
            bounds=DefaultScaraProfile.create_bounds()
        )
        self.validator = WaypointValidator(kinematics=kinematics)

    def test_validator_name(self) -> None:
        '''
            Verifies validator name identifier.
        '''
        self.assertEqual(self.validator.name, 'waypoint_validator')

    def test_validate_point_valid(self) -> None:
        '''
            Verifies that a valid reachable waypoint passes validation.
        '''
        wp = Waypoint(x=150.0, y=100.0, z=0.0, speed=50.0)
        res: ValidationResult = self.validator.validate_point(wp)
        self.assertTrue(res.is_valid)

    def test_validate_point_out_of_workspace_z(self) -> None:
        '''
            Verifies that a waypoint with Z out of bounds fails validation.
        '''
        wp = Waypoint(x=150.0, y=100.0, z=200.0, speed=50.0)
        res: ValidationResult = self.validator.validate_point(wp)
        self.assertFalse(res.is_valid)

    def test_validate_point_unreachable(self) -> None:
        '''
            Verifies that a waypoint beyond arm reach fails validation.
        '''
        wp = Waypoint(x=600.0, y=600.0, z=0.0, speed=50.0)
        res: ValidationResult = self.validator.validate_point(wp)
        self.assertFalse(res.is_valid)

    def test_validate_point_violates_joint_limits(self) -> None:
        '''
            Verifies that a waypoint violating joint angular limits fails validation.
        '''
        wp = Waypoint(x=40.0, y=0.0, z=10.0, speed=50.0)
        res: ValidationResult = self.validator.validate_point(wp)
        self.assertFalse(res.is_valid)
        self.assertIn('violates joint limits', res.message)

    def test_validate_point_kinematically_unreachable(self) -> None:
        '''
            Verifies that a point causing mathematical reach failure returns unreachable message.
        '''
        mock_kinematics = MagicMock(spec=IKinematicsService)
        mock_kinematics.is_in_workspace.return_value = (True, 'in workspace')
        mock_kinematics.is_joint_reachable.return_value = (
            False, ['Mathematically unreachable (cos_q2 > 1.0)']
        )
        validator = WaypointValidator(kinematics=mock_kinematics)
        res: ValidationResult = validator.validate_point(
            Waypoint(x=100.0, y=100.0, z=10.0, speed=50.0)
        )
        self.assertFalse(res.is_valid)
        self.assertIn('is kinematically unreachable', res.message)

    def test_validate_point_empty_reasons(self) -> None:
        '''
            Verifies fallback message when reasons list is empty.
        '''
        mock_kinematics = MagicMock(spec=IKinematicsService)
        mock_kinematics.is_in_workspace.return_value = (True, 'in workspace')
        mock_kinematics.is_joint_reachable.return_value = (False, [])
        validator = WaypointValidator(kinematics=mock_kinematics)
        res: ValidationResult = validator.validate_point(
            Waypoint(x=100.0, y=100.0, z=10.0, speed=50.0)
        )
        self.assertFalse(res.is_valid)
        self.assertIn('Joint limits exceeded', res.message)


if __name__ == '__main__':
    main()
