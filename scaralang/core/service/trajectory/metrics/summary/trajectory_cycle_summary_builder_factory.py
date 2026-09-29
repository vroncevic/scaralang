# -*- coding: UTF-8 -*-

'''
Module
    trajectory_cycle_summary_builder_factory.py
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
    Defines TrajectoryCycleSummaryBuilderFactory instantiating TrajectoryCycleSummaryBuilder.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.metrics.bottleneck.motion_bottleneck_detector_factory import MotionBottleneckDetectorFactory
from scaralang.core.service.trajectory.metrics.cycle.cycle_time_calculator_factory import CycleTimeCalculatorFactory
from scaralang.core.service.trajectory.metrics.profile.axis_speed_profile_analyzer_factory import AxisSpeedProfileAnalyzerFactory
from scaralang.core.service.trajectory.metrics.summary.itrajectory_cycle_summary_builder import ITrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.trajectory_cycle_summary_builder import TrajectoryCycleSummaryBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCycleSummaryBuilderFactory:
    '''
        Factory instantiating TrajectoryCycleSummaryBuilder with collaborating services.

        It defines:

            :methods:
                | create - Instantiates a new ITrajectoryCycleSummaryBuilder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ITrajectoryCycleSummaryBuilder:
        '''
            Creates a new ITrajectoryCycleSummaryBuilder instance using collaborator factories.

            :return: Fully configured ITrajectoryCycleSummaryBuilder instance.
        '''
        return TrajectoryCycleSummaryBuilder(
            cycle_time_calculator=CycleTimeCalculatorFactory.create(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzerFactory.create(),
            bottleneck_detector=MotionBottleneckDetectorFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
