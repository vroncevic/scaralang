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
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingSummaryBuilder:  # pylint: disable=too-few-public-methods
    '''Dummy class not implementing ITrajectoryCycleSummaryBuilder.'''


class TestITrajectoryCycleSummaryBuilder(TestCase):
    '''
        Test cases for ITrajectoryCycleSummaryBuilder structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies builder satisfies protocol.
                | test_factory_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_builder_name - Verifies builder name property.
    '''

    def _create_dependencies(self) -> SummaryDependencies:
        '''Helper constructing SummaryDependencies bundle.'''
        return SummaryDependencies(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )

    def test_structural_conformance(self) -> None:
        '''Verifies TrajectoryCycleSummaryBuilder satisfies protocol.'''
        deps = self._create_dependencies()
        builder = TrajectoryCycleSummaryBuilder(dependencies=deps)
        self.assertIsInstance(builder, ITrajectoryCycleSummaryBuilder)

    def test_factory_conformance(self) -> None:
        '''Verifies factory returns instance satisfying protocol.'''
        deps = self._create_dependencies()
        provides = SummaryFactory.create(dependencies=deps)
        self.assertIsInstance(provides.builder, ITrajectoryCycleSummaryBuilder)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingSummaryBuilder()
        self.assertNotIsInstance(dummy, ITrajectoryCycleSummaryBuilder)

    def test_builder_name(self) -> None:
        '''Verifies builder name property returns expected identifier string.'''
        deps = self._create_dependencies()
        builder = TrajectoryCycleSummaryBuilder(dependencies=deps)
        self.assertEqual(builder.name, 'trajectory_cycle_summary_builder')


if __name__ == '__main__':
    main()
