# -*- coding: UTF-8 -*-

'''
Module
    discretizer_test.py
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
    Unit tests for StepDiscretizer class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.joint_angles import JointAngles
from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.discretizer import StepDiscretizer
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStepDiscretizer(TestCase):
    '''
        Test cases verifying StepDiscretizer discretization.

        It defines:

            :methods:
                | setUp - Initializes StepDiscretizer fixture.
                | test_structural_conformance - Verifies protocol satisfaction.
                | test_angles_to_steps - Verifies conversion from angles to steps.
                | test_discretize_waypoint - Verifies Cartesian waypoint discretization.
                | test_discretize_unreachable_waypoint_raises_error - Verifies ScaraKinematicsError.
                | test_discretize_z_out_of_bounds_raises_error - Verifies Z limits error.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
        '''
        spatial = DefaultKinematicsFactory.create().spatial
        transmission = TransmissionFactory.create(
            transmission=DefaultScaraProfile.create_transmission()
        )
        duration_calculator = SegmentDurationCalculatorFactory.create()
        deps = DiscretizerDependencies(
            spatial=spatial,
            transmission=transmission,
            duration_calculator=duration_calculator,
        )
        self.discretizer = StepDiscretizer(dependencies=deps)

    def test_structural_conformance(self) -> None:
        '''
            Verifies that StepDiscretizer satisfies IStepDiscretizer.

            :exceptions: None.
        '''
        self.assertIsInstance(self.discretizer, IStepDiscretizer)

    def test_angles_to_steps(self) -> None:
        '''
            Verifies conversion from angles to discrete steps.

            :exceptions: None.
        '''
        steps: JointStepCoordinates = self.discretizer.angles_to_steps(0.0, 0.0, 10.0, 0.0)
        self.assertEqual(steps.j1, 0)
        self.assertEqual(steps.j2, 0)
        self.assertGreater(steps.z, 0)
        self.assertEqual(steps.j4, 0)

    def test_discretize_waypoint(self) -> None:
        '''
            Verifies Cartesian waypoint discretization into JointSteps.

            :exceptions: None.
        '''
        waypoint = Waypoint(
            x=150.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
            name='',
            command='',
        )
        joint_steps, new_angles = self.discretizer.discretize_waypoint(
            waypoint=waypoint,
            prev_angles=JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0),
        )
        self.assertIsInstance(joint_steps, JointSteps)
        self.assertGreater(joint_steps.duration_us, 0)
        self.assertIsInstance(new_angles, JointAngles)

    def test_discretize_unreachable_waypoint_raises_error(self) -> None:
        '''
            Verifies ScaraKinematicsError on unreachable waypoint.

            :exceptions: None.
        '''
        unreachable = Waypoint(
            x=99999.0,
            y=99999.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
            name='',
            command='',
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize_waypoint(
                waypoint=unreachable,
                prev_angles=JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0),
            )

    def test_discretize_z_out_of_bounds_raises_error(self) -> None:
        '''
            Verifies ScaraKinematicsError when waypoint Z is outside vertical travel bounds.

            :exceptions: None.
        '''
        z_invalid = Waypoint(
            x=150.0,
            y=50.0,
            z=-100.0,
            phi=0.0,
            speed=50.0,
            name='',
            command='',
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize_waypoint(
                waypoint=z_invalid,
                prev_angles=JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0),
            )

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self.discretizer.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
