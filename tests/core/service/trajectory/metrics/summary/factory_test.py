# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SummaryFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.bottleneck.detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.summary.dependencies import SummaryDependencies
from scaralang.core.service.trajectory.metrics.summary.factory import SummaryFactory
from scaralang.core.service.trajectory.metrics.summary.ibuilder import ITrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.provides import SummaryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSummaryFactory(TestCase):
    '''
        Test cases for SummaryFactory component creation.

        It defines:

            :attributes:
                | deps - SummaryDependencies test fixture.
            :methods:
                | setUp - Prepares SummaryDependencies fixture.
                | test_create - Verifies factory returns SummaryProvides bundle.
                | test_get_version - Verifies factory version string format.
    '''

    deps: SummaryDependencies

    def setUp(self) -> None:
        '''
            Prepares SummaryDependencies fixture.

            :exceptions: None.
        '''
        self.deps = SummaryDependencies(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )

    def test_create(self) -> None:
        '''
            Verifies factory instantiates and wires SummaryProvides bundle.

            :exceptions: None.
        '''
        bundle = SummaryFactory.create(dependencies=self.deps)
        self.assertIsInstance(bundle, SummaryProvides)
        self.assertIsInstance(bundle.builder, ITrajectoryCycleSummaryBuilder)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns valid semantic version string.

            :exceptions: None.
        '''
        version_str = SummaryFactory.get_version()
        self.assertIsInstance(version_str, str)
        self.assertTrue(len(version_str) > 0)


if __name__ == '__main__':
    main()
