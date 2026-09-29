# -*- coding: UTF-8 -*-

'''
Module
    binary_compiler.py
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
    Compiles trajectory plans into binary execution frames and binary programs.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.service.compiler.binary.metrics.ibinary_metrics_calculator import IBinaryMetricsCalculator
from scaralang.core.service.compiler.binary.step.iwaypoint_step_dispatcher import IWaypointStepDispatcher
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryCompiler:
    '''
        Compiles trajectory plans into binary programs using step dispatch and metrics calculation.

        It defines:

            :attributes:
                | _step_dispatcher - Waypoint step dispatcher protocol instance.
                | _metrics_calculator - Binary metrics calculator protocol instance.
            :methods:
                | __init__ - Initializes BinaryCompiler with injected collaborators.
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
    '''

    _step_dispatcher: IWaypointStepDispatcher
    _metrics_calculator: IBinaryMetricsCalculator

    def __init__(
        self,
        *,
        step_dispatcher: IWaypointStepDispatcher,
        metrics_calculator: IBinaryMetricsCalculator,
    ) -> None:
        '''
            Initializes BinaryCompiler with injected collaborators.

            :param step_dispatcher: Injected IWaypointStepDispatcher protocol instance.
            :param metrics_calculator: Injected IBinaryMetricsCalculator protocol instance.
            :exceptions: None.
        '''
        self._step_dispatcher = step_dispatcher
        self._metrics_calculator = metrics_calculator

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Compiled BinaryProgram containing binary frames and byte stream.
            :exceptions: None.
        '''
        steps: tuple[Step, ...] = self._step_dispatcher.dispatch_steps(
            waypoints=plan.waypoints
        )
        duration_us, step_counts = self._metrics_calculator.calculate_metrics(
            steps=steps
        )
        raw_bytes: bytes = b''.join(s.raw_bytes for s in steps)
        telemetry: BinaryProgramTelemetry = (
            self._metrics_calculator.calculate_telemetry(
                steps=steps, raw_bytes=raw_bytes
            )
        )

        return BinaryProgram(
            steps=steps,
            raw_bytes=raw_bytes,
            total_duration_us=duration_us,
            instruction_count=len(steps),
            step_counts=step_counts,
            telemetry=telemetry,
        )
