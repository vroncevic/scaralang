# -*- coding: UTF-8 -*-

'''
Module
    trajectory_cycle_summary_builder_test.py
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

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.trajectory.trajectory_cycle_report import TrajectoryCycleReport
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.trajectory.metrics.bottleneck.motion_bottleneck_detector import MotionBottleneckDetector
from scaralang.core.service.trajectory.metrics.cycle.cycle_time_calculator import CycleTimeCalculator
from scaralang.core.service.trajectory.metrics.profile.axis_speed_profile_analyzer import AxisSpeedProfileAnalyzer
from scaralang.core.service.trajectory.metrics.summary.itrajectory_cycle_summary_builder import ITrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.metrics.summary.trajectory_cycle_summary_builder import TrajectoryCycleSummaryBuilder
from scaralang.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryCycleSummaryBuilder(TestCase):
    '''Test suite verifying TrajectoryCycleSummaryBuilder report synthesis.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        builder: TrajectoryCycleSummaryBuilder = TrajectoryCycleSummaryBuilder(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )
        self.assertTrue(isinstance(builder, ITrajectoryCycleSummaryBuilder))

    def test_build_report_empty(self) -> None:
        '''Verifies report building with empty plan and program.'''
        builder: TrajectoryCycleSummaryBuilder = TrajectoryCycleSummaryBuilder(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )
        plan: TrajectoryPlan = TrajectoryPlan()
        program: BinaryProgram = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=BinaryProgramTelemetry(),
        )
        report: TrajectoryCycleReport = builder.build_report(plan=plan, program=program)
        self.assertEqual(report.total_duration_us, 0)
        self.assertEqual(report.total_distance_mm, 0.0)
        self.assertEqual(len(report.axis_peaks), 4)
        self.assertEqual(len(report.bottlenecks), 0)

    def test_build_report_populated(self) -> None:
        '''Verifies report generation with populated plan and program.'''
        builder: TrajectoryCycleSummaryBuilder = TrajectoryCycleSummaryBuilder(
            cycle_time_calculator=CycleTimeCalculator(),
            speed_profile_analyzer=AxisSpeedProfileAnalyzer(),
            bottleneck_detector=MotionBottleneckDetector(),
        )
        plan: TrajectoryPlan = TrajectoryPlan()
        plan.add_point(point=Waypoint(x=0.0, y=0.0, z=0.0, speed=100.0))
        plan.add_point(point=Waypoint(x=50.0, y=0.0, z=0.0, speed=100.0))

        frame: BinaryFrame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 16,
            crc16=0,
        )
        step: Step = Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=500000,
            target_steps=(2000, 100, 50, 0),
            description='move',
            line_number=1,
        )
        program: BinaryProgram = BinaryProgram(
            steps=(step,),
            raw_bytes=b'',
            total_duration_us=500000,
            instruction_count=1,
            step_counts=(2000, 100, 50, 0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=500000,
                duration_s=0.5,
            ),
        )
        report: TrajectoryCycleReport = builder.build_report(plan=plan, program=program)
        self.assertEqual(report.total_duration_us, 500000)
        self.assertAlmostEqual(report.total_distance_mm, 50.0, places=5)
        self.assertEqual(len(report.axis_peaks), 4)
        self.assertEqual(len(report.bottlenecks), 1)
        self.assertEqual(report.bottlenecks[0].limiting_axis, 'J1')


if __name__ == '__main__':
    main()
