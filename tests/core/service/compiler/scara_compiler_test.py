# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_test.py
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
    Unit tests for ScaraCompiler.
'''

from __future__ import annotations

from math import radians
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraCompiler(TestCase):
    '''
        Test cases verifying ScaraCompiler compilation and validation.

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
            l1=150.0,
            l2=150.0,
            z_min=-50.0,
            z_max=50.0,
            min_speed=1.0,
            max_speed=200.0,
            default_speed=50.0,
            default_accel=100.0,
            max_accel=500.0,
            j1_min_rad=radians(-150.0),
            j1_max_rad=radians(150.0),
            j2_min_rad=radians(-150.0),
            j2_max_rad=radians(150.0),
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=radians(5.0),
            deadzone_r_min=20.0,
        )
        kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        self.compiler = ScaraCompilerFactory.create(validator=validator)

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IScaraCompiler.
        '''
        self.assertIsInstance(self.compiler, IScaraCompiler)

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
            Verifies that unreachable coordinates trigger validation ValueError.
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
        with self.assertRaises(ValueError):
            self.compiler.compile(program=program)


if __name__ == '__main__':
    main()
