# -*- coding: UTF-8 -*-

'''
Module
    icalculator_test.py
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
    Unit tests for ISegmentDurationCalculator structural protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.joint_step_coordinates import JointStepCoordinates
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyDurationCalculator:
    '''
        Dummy class implementing ISegmentDurationCalculator for protocol verification.

        It defines:

            :methods:
                | calculate_duration - Dummy calculate_duration implementation.
                | get_version - Dummy get_version implementation.
    '''

    def calculate_duration(
        self,
        *,
        current_steps: JointStepCoordinates,
        target_steps: JointStepCoordinates,
        speed_mm_s: float,
    ) -> int:
        '''
            Dummy calculate_duration implementation.

            :param current_steps: Initial joint step coordinates.
            :param target_steps: Target joint step coordinates.
            :param speed_mm_s: Planned linear tool speed in mm/s.
            :return: Fixed dummy microsecond execution duration.
            :exceptions: None.
        '''
        _ = current_steps
        _ = target_steps
        _ = speed_mm_s
        return 10000

    def get_version(self) -> str:
        '''
            Dummy get_version implementation.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.9'


class TestISegmentDurationCalculator(TestCase):
    '''
        Test cases verifying ISegmentDurationCalculator structural protocol.

        It defines:

            :methods:
                | test_protocol_implementation - Verifies compliant class satisfies protocol.
                | test_structural_rejection - Verifies incomplete class fails protocol.
    '''

    def test_protocol_implementation(self) -> None:
        '''
            Verifies that compliant class satisfies ISegmentDurationCalculator.

            :exceptions: None.
        '''
        calculator = DummyDurationCalculator()
        self.assertIsInstance(calculator, ISegmentDurationCalculator)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that class missing required methods fails protocol check.

            :exceptions: None.
        '''
        class IncompleteDurationCalculator:
            '''Dummy incomplete duration calculator for negative test.'''

            @property
            def name(self) -> str:
                '''Returns dummy name.'''
                return 'incomplete'

            def is_ready(self) -> bool:
                '''Returns ready status.'''
                return True

        self.assertNotIsInstance(IncompleteDurationCalculator(), ISegmentDurationCalculator)


if __name__ == '__main__':
    main()
