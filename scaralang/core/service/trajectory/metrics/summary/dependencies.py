# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle dataclass encapsulating inbound dependencies for SummaryFactory.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.trajectory.metrics.bottleneck.idetector import IMotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.icalculator import ICycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.ianalyzer import IAxisSpeedProfileAnalyzer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class SummaryDependencies:
    '''
        Immutable parameter bundle encapsulating summary builder collaborators.

        It defines:

            :attributes:
                | cycle_time_calculator - Injected duration and distance calculator protocol instance.
                | speed_profile_analyzer - Injected axis velocity and acceleration profiler protocol instance.
                | bottleneck_detector - Injected motion bottleneck detector protocol instance.
    '''

    cycle_time_calculator: ICycleTimeCalculator
    speed_profile_analyzer: IAxisSpeedProfileAnalyzer
    bottleneck_detector: IMotionBottleneckDetector
