# -*- coding: UTF-8 -*-

'''
Module
    ibuilder_test.py
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
    Unit tests for ITrajectoryCycleSummaryBuilder protocol.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.metrics.bottleneck.detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.summary.builder import TrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.dependencies import SummaryDependencies
from scaralang.core.service.trajectory.metrics.summary.factory import SummaryFactory
from scaralang.core.service.trajectory.metrics.summary.ibuilder import ITrajectoryCycleSummaryBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITrajectoryCycleSummaryBuilder(TestCase):
    '''
        Test cases for ITrajectoryCycleSummaryBuilder structural protocol conformance.

        It defines:

            :attributes:
                | deps - SummaryDependencies test fixture.
            :methods:
                | setUp - Prepares SummaryDependencies fixture.
                | test_structural_conformance - Verifies builder satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_builder_name - Verifies builder name property.
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

    def test_structural_conformance(self) -> None:
        '''
            Verifies TrajectoryCycleSummaryBuilder satisfies protocol.

            :exceptions: None.
        '''
        builder = TrajectoryCycleSummaryBuilder(dependencies=self.deps)
        self.assertIsInstance(builder, ITrajectoryCycleSummaryBuilder)

    def test_factory_conformance(self) -> None:
        '''
            Verifies factory returns instance satisfying protocol.

            :exceptions: None.
        '''
        provides = SummaryFactory.create(dependencies=self.deps)
        self.assertIsInstance(provides.builder, ITrajectoryCycleSummaryBuilder)

    def test_non_conforming_instance(self) -> None:
        '''
            Verifies non-conforming object is rejected by runtime_checkable protocol.

            :exceptions: None.
        '''
        dummy = object()
        self.assertNotIsInstance(dummy, ITrajectoryCycleSummaryBuilder)

    def test_builder_name(self) -> None:
        '''
            Verifies builder name property returns expected identifier string.

            :exceptions: None.
        '''
        builder = TrajectoryCycleSummaryBuilder(dependencies=self.deps)
        self.assertEqual(builder.name, 'trajectory_cycle_summary_builder')


if __name__ == '__main__':
    main()
