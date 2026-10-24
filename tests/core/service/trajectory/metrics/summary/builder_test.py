# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit tests for TrajectoryCycleSummaryBuilder service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.core.model.kinematics.pose.steps import JointStepCoordinates
from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.trajectory.metrics.report import TrajectoryCycleReport
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.trajectory.metrics.bottleneck.detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.summary.builder import TrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.dependencies import SummaryDependencies
from scaralang.core.service.trajectory.plan.plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryCycleSummaryBuilder(TestCase):
    '''
        Test suite verifying TrajectoryCycleSummaryBuilder report synthesis.

        It defines:

            :attributes:
                | builder - TrajectoryCycleSummaryBuilder instance fixture.
            :methods:
                | setUp - Prepares TrajectoryCycleSummaryBuilder fixture.
                | test_name_property - Verifies name property returns expected string.
                | test_build_report_empty - Verifies report building with empty plan.
                | test_build_report_populated - Verifies report with populated plan.
    '''

    builder: TrajectoryCycleSummaryBuilder

    def setUp(self) -> None:
        '''
            Prepares TrajectoryCycleSummaryBuilder fixture.

            :exceptions: None.
        '''
        deps = SummaryDependencies(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )
        self.builder = TrajectoryCycleSummaryBuilder(dependencies=deps)

    def test_name_property(self) -> None:
        '''
            Verifies name property returns expected identifier string.

            :exceptions: None.
        '''
        self.assertEqual(self.builder.name, 'trajectory_cycle_summary_builder')

    def test_build_report_empty(self) -> None:
        '''
            Verifies report building with empty plan and program.

            :exceptions: None.
        '''
        plan = TrajectoryPlan(waypoints=())
        prog = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=0,
                compiled_steps=0,
                duration_us=0,
                duration_s=0.0,
                peak_steps=AxisPeakSteps(
                    peak_j1_steps=0,
                    peak_j2_steps=0,
                    peak_z_steps=0,
                    peak_j4_steps=0,
                ),
                total_wire_bytes=0,
            ),
        )
        report: TrajectoryCycleReport = self.builder.build_report(
            plan=plan, program=prog
        )
        self.assertEqual(report.total_duration_us, 0)
        self.assertEqual(report.total_distance_mm, 0.0)
        self.assertEqual(len(report.axis_peaks), 4)
        self.assertEqual(len(report.bottlenecks), 0)

    def test_build_report_populated(self) -> None:
        '''
            Verifies report generation with populated plan and program.

            :exceptions: None.
        '''
        plan = TrajectoryPlan(
            waypoints=(
                Waypoint(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
                Waypoint(
                    x=50.0,
                    y=0.0,
                    z=0.0,
                    phi=0.0,
                    speed=100.0,
                    name='',
                    command='',
                ),
            )
        )

        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        step = BinaryStep(
            frame=frame,
            raw_bytes=b'',
            duration_us=500000,
            target_steps=JointStepCoordinates(j1=2000, j2=100, z=50, j4=0),
            description='move',
            line_number=1,
        )
        prog = BinaryProgram(
            steps=(step,),
            raw_bytes=b'',
            total_duration_us=500000,
            instruction_count=1,
            step_counts=JointStepCoordinates(j1=2000, j2=100, z=50, j4=0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=500000,
                duration_s=0.5,
                peak_steps=AxisPeakSteps(
                    peak_j1_steps=2000,
                    peak_j2_steps=100,
                    peak_z_steps=50,
                    peak_j4_steps=0,
                ),
                total_wire_bytes=0,
            ),
        )
        report: TrajectoryCycleReport = self.builder.build_report(
            plan=plan, program=prog
        )
        self.assertEqual(report.total_duration_us, 500000)
        self.assertAlmostEqual(report.total_distance_mm, 50.0, places=5)
        self.assertEqual(len(report.axis_peaks), 4)
        self.assertEqual(len(report.bottlenecks), 1)
        self.assertEqual(report.bottlenecks[0].limiting_axis, 'J1')


if __name__ == '__main__':
    main()
