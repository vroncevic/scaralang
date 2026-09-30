# -*- coding: UTF-8 -*-

'''
Module
    motion_bottleneck_detector.py
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
    Defines MotionBottleneckDetector identifying axes constraining trajectory execution time.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.trajectory.bottleneck_incident import BottleneckIncident

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionBottleneckDetector:
    '''
        Detects which robot axis dictates move duration, identifying kinematic bottlenecks.

        It defines:

            :attributes:
                | name - Identifier name of the motion bottleneck detector.
            :methods:
                | __init__ - Initializes MotionBottleneckDetector instance.
                | detect_bottlenecks - Evaluates motion steps to identify limiting axes.
                | detect_step_bottleneck - Evaluates a single step displacement for bottlenecks.
    '''

    def __init__(self) -> None:
        '''
            Initializes MotionBottleneckDetector instance.
        '''

    @property
    def name(self) -> str:
        '''
            Gets the detector identifier name.

            :return: Detector name string.
        '''
        return 'motion_bottleneck_detector'

    def detect_step_bottleneck(
        self,
        *,
        step: Step,
        step_index: int,
        prev_coords: tuple[int, int, int, int]
    ) -> BottleneckIncident | None:
        '''
            Determines whether a motion step is constrained by an axis velocity or acceleration.

            :param step: Motion step under analysis.
            :param step_index: Index of step in execution sequence.
            :param prev_coords: Preceding joint step coordinates (j1, j2, z, j4).
            :return: BottleneckIncident if movement occurred, else None.
        '''
        deltas: tuple[int, int, int, int] = (
            abs(step.target_steps[0] - prev_coords[0]),
            abs(step.target_steps[1] - prev_coords[1]),
            abs(step.target_steps[2] - prev_coords[2]),
            abs(step.target_steps[3] - prev_coords[3]),
        )
        max_delta: int = max(deltas)

        if max_delta == 0:
            return None

        axis_names: tuple[str, str, str, str] = ('J1', 'J2', 'Z', 'J4')
        limiting_axis: str = axis_names[deltas.index(max_delta)]
        constraint_type: str = 'ACCELERATION' if step.duration_us <= 5000 else 'VELOCITY'

        return BottleneckIncident(
            step_index=step_index,
            limiting_axis=limiting_axis,
            constraint_type=constraint_type,
            duration_us=step.duration_us,
        )

    def detect_bottlenecks(self, *, steps: tuple[Step, ...]) -> tuple[BottleneckIncident, ...]:
        '''
            Evaluates sequence of steps to compile bottleneck incidents across trajectory.

            :param steps: Sequence of compiled binary motion steps.
            :return: Tuple of BottleneckIncident records.
        '''
        incidents: list[BottleneckIncident] = []
        prev_coords: tuple[int, int, int, int] = (0, 0, 0, 0)

        for index, step in enumerate(steps):
            incident: BottleneckIncident | None = self.detect_step_bottleneck(
                step=step,
                step_index=index,
                prev_coords=prev_coords,
            )

            if incident is not None:
                incidents.append(incident)

            prev_coords = step.target_steps

        return tuple(incidents)
