# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_compiler_test.py
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
    Unit tests for TrajectoryPlanCompiler.
'''

from __future__ import annotations

from math import radians
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.kinematics.joint_angle_bounds import JointAngleBounds
from scaralang.core.model.kinematics.link_dimensions import LinkDimensions
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.singularity_margins import SingularityMargins
from scaralang.core.model.kinematics.speed_limits import SpeedLimits
from scaralang.core.model.kinematics.vertical_bounds import VerticalBounds
from scaralang.core.service.compiler.plan.itrajectory_plan_compiler import ITrajectoryPlanCompiler
from scaralang.core.service.compiler.plan.trajectory_plan_compiler_factory import TrajectoryPlanCompilerFactory
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryPlanCompiler(TestCase):
    '''
        Test cases verifying TrajectoryPlanCompiler compilation and validation.

        It defines:

            :methods:
                | setUp - Initializes test bounds and compiler.
                | test_structural_conformance - Verifies protocol check.
                | test_compile_valid_program - Tests successful compilation to ITrajectoryPlan.
                | test_compile_kinematic_failure - Tests exception on unreachable position.
    '''

    def setUp(self) -> None:
        '''
            Sets up test bounds, validator, and compiler.
        '''
        self.bounds = ScaraBounds(
            links=LinkDimensions(l1=150.0, l2=150.0),
            vertical=VerticalBounds(z_min=-50.0, z_max=50.0),
            speeds=SpeedLimits(
                min_speed=1.0,
                max_speed=200.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=radians(-150.0),
                j1_max_rad=radians(150.0),
                j2_min_rad=radians(-150.0),
                j2_max_rad=radians(150.0),
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=5.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=radians(5.0),
                deadzone_r_min=20.0,
            ),
        )
        kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        self.compiler = TrajectoryPlanCompilerFactory.create(validator=validator)

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to ITrajectoryPlanCompiler.
        '''
        self.assertIsInstance(self.compiler, ITrajectoryPlanCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies compiler get_version returns semantic version string.
        '''
        self.assertEqual(self.compiler.get_version(), '1.0.5')

    def test_compile_valid_program(self) -> None:
        '''
            Verifies compiling valid program produces ITrajectoryPlan.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_J,
                parameters={'X': 150.0, 'Y': 50.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_J X=150 Y=50 Z=20 PHI=0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        plan: ITrajectoryPlan = self.compiler.compile(program=program)
        self.assertIsInstance(plan, ITrajectoryPlan)
        self.assertGreaterEqual(plan.count, 2)

    def test_compile_kinematic_failure(self) -> None:
        '''
            Verifies that unreachable coordinates trigger validation ScaraKinematicsError.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_J,
                parameters={'X': 500.0, 'Y': 500.0, 'Z': 0.0, 'PHI': 0.0},
                line_number=1,
                raw_text='MOVE_J X=500 Y=500 Z=0 PHI=0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        with self.assertRaises(ScaraKinematicsError):
            self.compiler.compile(program=program)


if __name__ == '__main__':
    main()
