# -*- coding: UTF-8 -*-

'''
Module
    singularity_compiler_test.py
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
    Unit tests verifying compiler and validator singularity error handling and reach bounds.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.exceptions.kinematics import ScaraKinematicsError
from scaralang.core.service.compiler.plan.ast.factory import AstPlanCompilerFactory
from scaralang.core.service.compiler.plan.ast.icompiler import IAstPlanCompiler
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan
from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSingularityCompiler(TestCase):
    '''
        Test cases verifying compiler rejection of singularities and successful multi-elbow compilation.

        It defines:

            :methods:
                | setUp - Initializes test AST plan compiler with default kinematics.
                | test_outer_singularity_deadband_rejection - Verifies error at boundary J2=0 singularity.
                | test_outer_reach_exceeded_rejection - Verifies error when coordinates exceed R_max.
                | test_inner_deadzone_rejection - Verifies error when coordinates fall inside deadzone.
                | test_multi_elbow_transition_success - Verifies compilation with multi-elbow switching.
    '''

    compiler: IAstPlanCompiler

    def setUp(self) -> None:
        '''
            Sets up test kinematic bounds, validator, and compiler.

            :exceptions: None.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        dls_config = DefaultScaraProfile.create_dls_config()
        kinematics = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=dls_config,
            )
        )
        validation = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics.workspace,
                envelope=kinematics.envelope,
            )
        )
        self.compiler = AstPlanCompilerFactory.create(
            validator=validation.plan
        )

    def test_outer_singularity_deadband_rejection(self) -> None:
        '''
            Verifies that points at outer boundary singularity deadband raise ScaraKinematicsError.

            :exceptions: None.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                parameters={'X': 300.0, 'Y': 0.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_L X=300.0 Y=0.0 Z=20.0 PHI=0.0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        with self.assertRaises(ScaraKinematicsError) as ctx:
            self.compiler.compile(program=program)
        self.assertIn('singularity deadband', str(ctx.exception))

    def test_outer_reach_exceeded_rejection(self) -> None:
        '''
            Verifies that coordinates beyond physical reach radius raise ScaraKinematicsError.

            :exceptions: None.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                parameters={'X': 320.0, 'Y': 0.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_L X=320.0 Y=0.0 Z=20.0 PHI=0.0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        with self.assertRaises(ScaraKinematicsError) as ctx:
            self.compiler.compile(program=program)
        self.assertIn('exceeds maximum reach', str(ctx.exception))

    def test_inner_deadzone_rejection(self) -> None:
        '''
            Verifies that coordinates inside central dead zone raise ScaraKinematicsError.

            :exceptions: None.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                parameters={'X': 10.0, 'Y': 10.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_L X=10.0 Y=10.0 Z=20.0 PHI=0.0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        with self.assertRaises(ScaraKinematicsError) as ctx:
            self.compiler.compile(program=program)
        self.assertIn('inside deadzone', str(ctx.exception))

    def test_multi_elbow_transition_success(self) -> None:
        '''
            Verifies that programs with elbow configuration changes compile successfully.

            :exceptions: None.
        '''
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CONFIG_ELBOW,
                parameters={ScaraInstructionParam.ELBOW: 'RIGHT'},
                line_number=2,
                raw_text='CONFIG ELBOW RIGHT',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                parameters={'X': 150.0, 'Y': -150.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=3,
                raw_text='MOVE_L X=150.0 Y=-150.0 Z=20.0 PHI=0.0',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CONFIG_ELBOW,
                parameters={ScaraInstructionParam.ELBOW: 'LEFT'},
                line_number=4,
                raw_text='CONFIG ELBOW LEFT',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                parameters={'X': -248.3, 'Y': -87.8, 'Z': 20.0, 'PHI': 0.0},
                line_number=5,
                raw_text='MOVE_L X=-248.3 Y=-87.8 Z=20.0 PHI=0.0',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        plan: ITrajectoryPlan = self.compiler.compile(program=program)
        self.assertIsInstance(plan, ITrajectoryPlan)
        self.assertGreaterEqual(plan.count, 3)


if __name__ == '__main__':
    main()
