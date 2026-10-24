# -*- coding: UTF-8 -*-

'''
Module
    detector.py
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

from typing import ClassVar

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.axis import AxisName
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.trajectory.metrics.bottleneck import BottleneckIncident
from scaralang.core.model.trajectory.metrics.constraint import ConstraintType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionBottleneckDetector:
    '''
        Detects which robot axis dictates move duration, identifying kinematic bottlenecks.

        It defines:

            :attributes:
                | NAME - Canonical component identifier name.
                | ZERO_DELTA - Zero step movement threshold.
                | INITIAL_COORDS - Initial joint step coordinate tuple.
                | _ACCEL_DURATION_THRESHOLD_US - Maximum step duration in us considered acceleration-constrained.
                | _AXIS_NAMES - Canonical tuple of 4-DOF manipulator axis identity enums.
                | name - Identifier name of the motion bottleneck detector.
            :methods:
                | detect_bottlenecks - Evaluates motion steps to identify limiting axes.
                | detect_step_bottleneck - Evaluates a single step displacement for bottlenecks.
    '''

    NAME: ClassVar[str] = 'motion_bottleneck_detector'
    ZERO_DELTA: ClassVar[int] = 0
    INITIAL_COORDS: ClassVar[JointStepCoordinates] = JointStepCoordinates(
        j1=0, j2=0, z=0, j4=0
    )

    _ACCEL_DURATION_THRESHOLD_US: ClassVar[int] = 5000
    _AXIS_NAMES: ClassVar[tuple[AxisName, AxisName, AxisName, AxisName]] = (
        AxisName.J1,
        AxisName.J2,
        AxisName.Z,
        AxisName.J4,
    )

    @property
    def name(self) -> str:
        '''
            Gets the detector identifier name.

            :return: Detector name string.
        '''
        return self.NAME

    def detect_step_bottleneck(
        self,
        *,
        step: BinaryStep,
        step_index: int,
        prev_coords: JointStepCoordinates,
    ) -> tuple[BottleneckIncident, ...]:
        '''
            Determines whether a motion step is constrained by an axis velocity or acceleration.

            :param step: Motion step under analysis.
            :param step_index: Index of step in execution sequence.
            :param prev_coords: Preceding joint step coordinates (j1, j2, z, j4).
            :return: Tuple containing BottleneckIncident if movement occurred, empty tuple otherwise.
            :exceptions: None.
        '''
        deltas: tuple[int, int, int, int] = (
            abs(step.target_steps.j1 - prev_coords.j1),
            abs(step.target_steps.j2 - prev_coords.j2),
            abs(step.target_steps.z - prev_coords.z),
            abs(step.target_steps.j4 - prev_coords.j4),
        )
        max_delta: int = max(deltas)

        if max_delta == self.ZERO_DELTA:
            return ()

        limiting_axis: AxisName = self._AXIS_NAMES[deltas.index(max_delta)]
        constraint_type: ConstraintType = (
            ConstraintType.ACCELERATION
            if step.duration_us <= self._ACCEL_DURATION_THRESHOLD_US
            else ConstraintType.VELOCITY
        )

        return (
            BottleneckIncident(
                step_index=step_index,
                limiting_axis=limiting_axis,
                constraint_type=constraint_type,
                duration_us=step.duration_us,
            ),
        )

    def detect_bottlenecks(self, *, steps: tuple[BinaryStep, ...]) -> tuple[BottleneckIncident, ...]:
        '''
            Evaluates sequence of steps to compile bottleneck incidents across trajectory.

            :param steps: Sequence of compiled binary motion steps.
            :return: Tuple of BottleneckIncident records.
            :exceptions: None.
        '''
        incidents: list[BottleneckIncident] = []
        prev_coords: JointStepCoordinates = self.INITIAL_COORDS

        for index, step in enumerate(steps):
            incidents.extend(
                self.detect_step_bottleneck(
                    step=step,
                    step_index=index,
                    prev_coords=prev_coords,
                )
            )
            prev_coords = step.target_steps

        return tuple(incidents)
