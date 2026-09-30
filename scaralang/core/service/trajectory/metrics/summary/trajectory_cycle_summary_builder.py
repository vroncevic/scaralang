# -*- coding: UTF-8 -*-

'''
Module
    trajectory_cycle_summary_builder.py
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
    Defines TrajectoryCycleSummaryBuilder building comprehensive trajectory cycle telemetry reports.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric
from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident
from scaralang.core.model.trajectory.trajectory_cycle_report import TrajectoryCycleReport
from scaralang.core.service.trajectory.metrics.bottleneck.imotion_bottleneck_detector import IMotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.icycle_time_calculator import ICycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.iaxis_speed_profile_analyzer import IAxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCycleSummaryBuilder:
    '''
        Synthesizes duration calculations, axis peaks, and motion bottlenecks into reports.

        It defines:

            :attributes:
                | name - Identifier name of the summary builder.
                | _cycle_time_calculator - Injected cycle duration and distance calculator.
                | _speed_profile_analyzer - Injected axis speed and acceleration profiler.
                | _bottleneck_detector - Injected motion bottleneck detector.
            :methods:
                | __init__ - Initializes builder with collaborating metric services.
                | build_report - Synthesizes comprehensive TrajectoryCycleReport domain model.
    '''

    _cycle_time_calculator: ICycleTimeCalculator
    _speed_profile_analyzer: IAxisSpeedProfileAnalyzer
    _bottleneck_detector: IMotionBottleneckDetector

    def __init__(
        self,
        *,
        cycle_time_calculator: ICycleTimeCalculator,
        speed_profile_analyzer: IAxisSpeedProfileAnalyzer,
        bottleneck_detector: IMotionBottleneckDetector
    ) -> None:
        '''
            Initializes TrajectoryCycleSummaryBuilder with injected collaborator services.

            :param cycle_time_calculator: Injected duration and distance calculator.
            :param speed_profile_analyzer: Injected axis velocity and acceleration profiler.
            :param bottleneck_detector: Injected motion bottleneck detector.
        '''
        self._cycle_time_calculator: Final[ICycleTimeCalculator] = cycle_time_calculator
        self._speed_profile_analyzer: Final[IAxisSpeedProfileAnalyzer] = speed_profile_analyzer
        self._bottleneck_detector: Final[IMotionBottleneckDetector] = bottleneck_detector

    @property
    def name(self) -> str:
        '''
            Gets the summary builder identifier name.

            :return: Builder name string.
        '''
        return 'trajectory_cycle_summary_builder'

    def build_report(
        self,
        *,
        plan: ITrajectoryPlan,
        program: BinaryProgram
    ) -> TrajectoryCycleReport:
        '''
            Aggregates timing calculations, kinematic peaks, and bottlenecks into report.

            :param plan: Source trajectory plan with waypoints.
            :param program: Compiled binary program with execution steps.
            :return: TrajectoryCycleReport containing comprehensive metrics.
        '''
        duration_us: int = (
            program.total_duration_us
            if program.total_duration_us > 0
            else self._cycle_time_calculator.calculate_duration(plan=plan)
        )
        distance_mm: float = self._cycle_time_calculator.calculate_distance(plan=plan)
        peaks: tuple[AxisPeakMetric, ...] = self._speed_profile_analyzer.analyze_axis_peaks(
            steps=program.steps
        )
        bottlenecks: tuple[BottleneckIncident, ...] = (
            self._bottleneck_detector.detect_bottlenecks(steps=program.steps)
        )

        return TrajectoryCycleReport(
            total_duration_us=duration_us,
            total_distance_mm=distance_mm,
            axis_peaks=peaks,
            bottlenecks=bottlenecks,
        )
