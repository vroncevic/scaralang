# -*- coding: UTF-8 -*-

'''
Module
    istep_discretizer_test.py
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

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.binary.step.istep_discretizer import IStepDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyStepDiscretizer:
    '''
        Dummy class implementing IStepDiscretizer for protocol verification.
    '''

    @property
    def name(self) -> str:
        '''
            Returns dummy name.
        '''
        return 'dummy'

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: tuple[float, float, float, float]
    ) -> tuple[JointSteps, tuple[float, float, float, float]]:
        '''
            Dummy implementation of discretize_waypoint.
        '''
        _ = (waypoint, prev_angles)
        steps = JointSteps(
            target_j1_steps=0,
            target_j2_steps=0,
            target_z_steps=0,
            target_j4_steps=0,
            duration_us=1000,
            feedrate_scale=100,
        )
        return steps, (0.0, 0.0, 0.0, 0.0)

    def calculate_segment_duration(
        self,
        *,
        current_steps: tuple[int, int, int, int],
        target_steps: tuple[int, int, int, int],
        speed_mm_s: float
    ) -> int:
        '''
            Dummy implementation of calculate_segment_duration.
        '''
        _ = (current_steps, target_steps, speed_mm_s)
        return 1000


class TestIStepDiscretizer(TestCase):
    '''
        Test cases verifying IStepDiscretizer structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies that dummy conforming class satisfies protocol check.
        '''
        discretizer = DummyStepDiscretizer()
        self.assertIsInstance(discretizer, IStepDiscretizer)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that class missing required methods fails protocol check.
        '''
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
