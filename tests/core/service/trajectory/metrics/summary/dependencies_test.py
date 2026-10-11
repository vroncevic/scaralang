# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for SummaryDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.bottleneck.detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.summary.dependencies import SummaryDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSummaryDependencies(TestCase):
    '''
        Test cases for SummaryDependencies parameter bundle.

        It defines:

            :methods:
                | test_bundle_initialization - Verifies attributes initialized correctly.
                | test_bundle_immutability - Verifies FrozenInstanceError on modification.
    '''

    def test_bundle_initialization(self) -> None:
        '''Verifies bundle holds injected collaborator service instances.'''
        cycle_calc = CycleTimeCalculator()
        speed_ana = AxisSpeedProfileAnalyzer()
        b_detector = MotionBottleneckDetector()
        bundle = SummaryDependencies(
            cycle_time_calculator=cycle_calc,
            speed_profile_analyzer=speed_ana,
            bottleneck_detector=b_detector,
        )
        self.assertIs(bundle.cycle_time_calculator, cycle_calc)
        self.assertIs(bundle.speed_profile_analyzer, speed_ana)
        self.assertIs(bundle.bottleneck_detector, b_detector)

    def test_bundle_immutability(self) -> None:
        '''Verifies frozen dataclass rejects attribute mutations.'''
        cycle_calc = CycleTimeCalculator()
        speed_ana = AxisSpeedProfileAnalyzer()
        b_detector = MotionBottleneckDetector()
        bundle = SummaryDependencies(
            cycle_time_calculator=cycle_calc,
            speed_profile_analyzer=speed_ana,
            bottleneck_detector=b_detector,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.cycle_time_calculator = cycle_calc  # type: ignore[misc]


if __name__ == '__main__':
    main()
