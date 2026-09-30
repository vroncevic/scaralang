# -*- coding: UTF-8 -*-

'''
Module
    iaxis_speed_profile_analyzer.py
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
    Defines structural interface protocol for joint axis speed profile analysis.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.axis_peak_metric import AxisPeakMetric

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IAxisSpeedProfileAnalyzer(Protocol):
    '''
        Structural interface protocol for profiling joint velocities and accelerations.

        It defines:

            :attributes:
                | name - Identifier name of the speed profile analyzer.
            :methods:
                | analyze_axis_peaks - Analyzes steps to determine peak kinematic measurements.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the analyzer identifier name.

            :return: Analyzer name string.
        '''

    def analyze_axis_peaks(self, *, steps: tuple[Step, ...]) -> tuple[AxisPeakMetric, ...]:
        '''
            Analyzes joint step execution to compute peak velocity, acceleration, and microsteps.

            :param steps: Sequence of compiled binary motion steps.
            :return: Tuple of AxisPeakMetric records for each robot axis.
        '''
