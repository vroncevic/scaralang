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

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.discretizer import StepDiscretizer
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.transmission.factory import JointStepTransmissionConverterFactory
from scaralang.infrastructure.kinematics.factory import DefaultKinematicsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStepDiscretizer(TestCase):
    '''
        Test cases verifying StepDiscretizer discretization and duration calculation.

        It defines:

            :methods:
                | setUp - Initializes StepDiscretizer fixture.
                | test_structural_conformance - Verifies protocol satisfaction.
                | test_angles_to_steps - Verifies conversion from angles to steps.
                | test_discretize_waypoint - Verifies Cartesian waypoint discretization.
                | test_calculate_segment_duration - Verifies segment duration calculation.
                | test_discretize_unreachable_waypoint_raises_error - Verifies ScaraKinematicsError.
                | test_calculate_segment_duration_zero_delta - Verifies default duration for zero delta.
                | test_get_version - Verifies implementation version string.
    '''

    def setUp(self) -> None:
        '''Sets up test fixtures.'''
        kinematics = DefaultKinematicsFactory.create().service
        transmission = JointStepTransmissionConverterFactory.create(
            transmission=DefaultScaraProfile.create_transmission()
        )
        deps = DiscretizerDependencies(
            kinematics=kinematics,
            transmission=transmission,
        )
        self.discretizer = StepDiscretizer(dependencies=deps)

    def test_structural_conformance(self) -> None:
        '''Verifies that StepDiscretizer satisfies IStepDiscretizer.'''
        self.assertIsInstance(self.discretizer, IStepDiscretizer)

    def test_angles_to_steps(self) -> None:
        '''Verifies conversion from angles to discrete steps.'''
        steps = self.discretizer.angles_to_steps(0.0, 0.0, 10.0, 0.0)
        self.assertEqual(len(steps), 4)
        self.assertEqual(steps[0], 0)
        self.assertEqual(steps[1], 0)
        self.assertGreater(steps[2], 0)
        self.assertEqual(steps[3], 0)

    def test_discretize_waypoint(self) -> None:
        '''Verifies Cartesian waypoint discretization into JointSteps.'''
        waypoint = Waypoint(
            x=150.0,
            y=50.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
        )
        joint_steps, new_angles = self.discretizer.discretize_waypoint(
            waypoint=waypoint,
            prev_angles=(0.0, 0.0, 0.0, 0.0),
        )
        self.assertIsInstance(joint_steps, JointSteps)
        self.assertGreater(joint_steps.duration_us, 0)
        self.assertEqual(len(new_angles), 4)

    def test_calculate_segment_duration(self) -> None:
        '''Verifies duration calculation in microseconds.'''
        duration_us = self.discretizer.calculate_segment_duration(
            current_steps=(0, 0, 0, 0),
            target_steps=(1000, 1000, 500, 200),
            speed_mm_s=50.0,
        )
        self.assertGreater(duration_us, 0)

    def test_discretize_unreachable_waypoint_raises_error(self) -> None:
        '''Verifies ScaraKinematicsError on unreachable waypoint.'''
        unreachable = Waypoint(
            x=99999.0,
            y=99999.0,
            z=10.0,
            phi=0.0,
            speed=50.0,
        )
        with self.assertRaises(ScaraKinematicsError):
            self.discretizer.discretize_waypoint(
                waypoint=unreachable,
                prev_angles=(0.0, 0.0, 0.0, 0.0),
            )

    def test_calculate_segment_duration_zero_delta(self) -> None:
        '''Verifies duration is 1000 us when start and target steps are identical.'''
        duration_us = self.discretizer.calculate_segment_duration(
            current_steps=(100, 100, 100, 100),
            target_steps=(100, 100, 100, 100),
            speed_mm_s=50.0,
        )
        self.assertEqual(duration_us, 1000)

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid version string.'''
        self.assertEqual(self.discretizer.get_version(), '1.0.8')


if __name__ == '__main__':
    main()
