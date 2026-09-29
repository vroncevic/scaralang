# -*- coding: UTF-8 -*-

'''
Module
    step_discretizer_test.py
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

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.istep_discretizer import IStepDiscretizer
from scaralang.core.service.compiler.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.kinematics.transmission.joint_step_transmission_converter_factory import JointStepTransmissionConverterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
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
                | test_calculate_segment_duration - Verifies segment execution duration calculation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        transmission = JointStepTransmissionConverterFactory.create_default()
        self.discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            kinematics=kinematics,
            transmission=transmission,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies that StepDiscretizer satisfies IStepDiscretizer.
        '''
        self.assertIsInstance(self.discretizer, IStepDiscretizer)

    def test_angles_to_steps(self) -> None:
        '''
            Verifies conversion from angles to discrete steps.
        '''
        steps = self.discretizer.angles_to_steps(0.0, 0.0, 10.0, 0.0)
        self.assertEqual(len(steps), 4)
        self.assertEqual(steps[0], 0)
        self.assertEqual(steps[1], 0)
        self.assertGreater(steps[2], 0)
        self.assertEqual(steps[3], 0)

    def test_discretize_waypoint(self) -> None:
        '''
            Verifies Cartesian waypoint discretization into JointSteps.
        '''
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
        '''
            Verifies duration calculation in microseconds.
        '''
        duration_us = self.discretizer.calculate_segment_duration(
            current_steps=(0, 0, 0, 0),
            target_steps=(1000, 1000, 500, 200),
            speed_mm_s=50.0,
        )
        self.assertGreater(duration_us, 0)


if __name__ == '__main__':
    main()
