# -*- coding: UTF-8 -*-

'''
Module
    idiscretizer_test.py
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
    Unit tests for IStepDiscretizer protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.joint_angles import JointAngles
from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.discretizer.idiscretizer import IStepDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyStepDiscretizer:
    '''
        Dummy class implementing IStepDiscretizer for protocol verification.
    '''

    @property
    def name(self) -> str:
        '''Returns dummy name.'''
        return 'dummy'

    def angles_to_steps(
        self,
        theta1_rad: float,
        theta2_rad: float,
        z_mm: float,
        theta4_rad: float,
    ) -> JointStepCoordinates:
        '''Dummy implementation of angles_to_steps.'''
        _ = (theta1_rad, theta2_rad, z_mm, theta4_rad)
        return JointStepCoordinates(j1=0, j2=0, z=0, j4=0)

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: JointAngles,
    ) -> tuple[JointSteps, JointAngles]:
        '''Dummy implementation of discretize_waypoint.'''
        _ = (waypoint, prev_angles)
        steps = JointSteps(
            target_j1_steps=0,
            target_j2_steps=0,
            target_z_steps=0,
            target_j4_steps=0,
            duration_us=1000,
            feedrate_scale=100,
        )
        return steps, JointAngles(theta1=0.0, theta2=0.0, z=0.0, theta4=0.0)

    def get_version(self) -> str:
        '''Dummy implementation of get_version.'''
        return '1.0.0'


class TestIStepDiscretizer(TestCase):
    '''
        Test cases verifying IStepDiscretizer structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies that dummy conforming class satisfies protocol check.'''
        discretizer = DummyStepDiscretizer()
        self.assertIsInstance(discretizer, IStepDiscretizer)

    def test_structural_rejection(self) -> None:
        '''Verifies that class missing required methods fails protocol check.'''
        class IncompleteDiscretizer:
            '''Dummy incomplete discretizer for negative test.'''

            @property
            def name(self) -> str:
                '''Returns dummy name.'''
                return 'incomplete'

            def is_ready(self) -> bool:
                '''Returns ready status.'''
                return True

        self.assertNotIsInstance(IncompleteDiscretizer(), IStepDiscretizer)


if __name__ == '__main__':
    main()
