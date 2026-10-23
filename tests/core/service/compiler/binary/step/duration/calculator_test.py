# -*- coding: UTF-8 -*-

'''
Module
    calculator_test.py
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
    Unit tests for SegmentDurationCalculator class.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.service.compiler.binary.step.duration.calculator import SegmentDurationCalculator
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSegmentDurationCalculator(TestCase):
    '''
        Test cases verifying SegmentDurationCalculator duration computations.

        It defines:

            :methods:
                | setUp - Initializes calculator test fixture.
                | test_satisfies_protocol - Verifies class satisfies ISegmentDurationCalculator.
                | test_calculate_duration_standard - Verifies nominal segment duration calculation.
                | test_calculate_duration_zero_delta - Verifies idle duration for stationary segments.
                | test_calculate_duration_low_speed_clamping - Verifies speed clamping threshold.
                | test_calculate_duration_min_duration_floor - Verifies minimum duration threshold.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes calculator test fixture.

            :exceptions: None.
        '''
        self.calculator = SegmentDurationCalculator()

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies that SegmentDurationCalculator satisfies ISegmentDurationCalculator.

            :exceptions: None.
        '''
        self.assertIsInstance(self.calculator, ISegmentDurationCalculator)

    def test_calculate_duration_standard(self) -> None:
        '''
            Verifies nominal segment duration calculation.

            :exceptions: None.
        '''
        current = JointStepCoordinates(j1=0, j2=0, z=0, j4=0)
        target = JointStepCoordinates(j1=1000, j2=1000, z=500, j4=200)
        duration_us = self.calculator.calculate_duration(
            current_steps=current,
            target_steps=target,
            speed_mm_s=100.0,
        )
        self.assertEqual(duration_us, 1000000)

    def test_calculate_duration_zero_delta(self) -> None:
        '''
            Verifies idle duration for stationary segments.

            :exceptions: None.
        '''
        coords = JointStepCoordinates(j1=100, j2=100, z=100, j4=100)
        duration_us = self.calculator.calculate_duration(
            current_steps=coords,
            target_steps=coords,
            speed_mm_s=100.0,
        )
        self.assertEqual(duration_us, 1000)

    def test_calculate_duration_low_speed_clamping(self) -> None:
        '''
            Verifies speed clamping threshold.

            :exceptions: None.
        '''
        current = JointStepCoordinates(j1=0, j2=0, z=0, j4=0)
        target = JointStepCoordinates(j1=10, j2=0, z=0, j4=0)
        duration_us = self.calculator.calculate_duration(
            current_steps=current,
            target_steps=target,
            speed_mm_s=0.01,
        )
        self.assertGreaterEqual(duration_us, 5000)

    def test_calculate_duration_min_duration_floor(self) -> None:
        '''
            Verifies minimum duration threshold.

            :exceptions: None.
        '''
        current = JointStepCoordinates(j1=0, j2=0, z=0, j4=0)
        target = JointStepCoordinates(j1=1, j2=0, z=0, j4=0)
        duration_us = self.calculator.calculate_duration(
            current_steps=current,
            target_steps=target,
            speed_mm_s=1000.0,
        )
        self.assertEqual(duration_us, 5000)

    def test_get_version(self) -> None:
        '''
            Verifies implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self.calculator.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
