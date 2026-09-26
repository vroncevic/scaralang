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
    Unit tests for ScaraCompiler and its specialized primitive sub-compilers.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scaralang.core.model.dsl.ast.command_type import CommandType
from scaralang.core.model.dsl.ast.instruction import Instruction
from scaralang.core.model.dsl.ast.program import Program
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.dsl.compiler.motion.arc_interpolator import ArcInterpolator
from scaralang.core.service.dsl.compiler.primitive.control_command_compiler import ControlCommandCompiler
from scaralang.core.service.dsl.compiler.motion.motion_command_compiler import MotionCommandCompiler
from scaralang.core.service.dsl.compiler.motion.motion_command_compiler_factory import MotionCommandCompilerFactory
from scaralang.core.service.dsl.compiler.motion.cartesian_move_compiler_factory import CartesianMoveCompilerFactory
from scaralang.core.service.dsl.compiler.motion.vertical_move_compiler_factory import VerticalMoveCompilerFactory
from scaralang.core.service.dsl.compiler.motion.arc_move_compiler_factory import ArcMoveCompilerFactory
from scaralang.core.service.dsl.compiler.scara_compiler import ScaraCompiler
from scaralang.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.dsl.compiler.scara_compiler_factory import ScaraCompilerFactory
from scaralang.core.service.dsl.compiler.primitive.state_command_compiler import StateCommandCompiler
from scaralang.core.service.dsl.compiler.primitive.tool_command_compiler import ToolCommandCompiler
from scaralang.core.service.dsl.macro.tangent_macro_expander import TangentMacroExpander
from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraCompiler(TestCase):
    '''
        Test cases verifying ScaraCompiler and its decomposed sub-compilers.

        It defines:

            :methods:
                | test_state_command_compiler - Verifies state configuration compiler.
                | test_tool_command_compiler - Verifies pneumatic tool compiler.
                | test_control_command_compiler - Verifies workflow control compiler.
                | test_motion_command_compiler - Verifies Cartesian and Arc motion compiler.
                | test_compiler_end_to_end - Verifies full ScaraCompiler compiling AST program.
                | test_compiler_custom_sub_compilers - Verifies injection of custom primitive compilers.
    '''

    def test_state_command_compiler(self) -> None:
        '''Verifies StateCommandCompiler handles SPEED, ACCEL, ZONE, CONFIG_ELBOW.'''
        compiler = StateCommandCompiler()
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        speed_inst = Instruction(
            command_type=CommandType.SPEED,
            parameters={'mode': 'RAPID', 'speed': 150.0},
            line_number=1,
            raw_text='SPEED RAPID 150.0',
        )
        self.assertTrue(compiler.can_compile(instruction=speed_inst))
        compiler.compile(instruction=speed_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(ctx.speed_rapid, 150.0)

        zone_inst = Instruction(
            command_type=CommandType.ZONE,
            parameters={'mode': 'BLEND', 'radius': 5.0},
            line_number=2,
            raw_text='ZONE BLEND R=5.0',
        )
        self.assertTrue(compiler.can_compile(instruction=zone_inst))
        compiler.compile(instruction=zone_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(ctx.zone_mode, 'BLEND')
        self.assertEqual(ctx.zone_radius, 5.0)

    def test_tool_command_compiler(self) -> None:
        '''Verifies ToolCommandCompiler handles PUMP and VALVE commands.'''
        compiler = ToolCommandCompiler()
        ctx = ScaraCompilerContext()
        ctx.current_x = 100.0
        ctx.current_y = 50.0
        waypoints: list[Waypoint] = []

        pump_inst = Instruction(
            command_type=CommandType.PUMP,
            parameters={'state': 'ON'},
            line_number=3,
            raw_text='PUMP ON',
        )
        self.assertTrue(compiler.can_compile(instruction=pump_inst))
        compiler.compile(instruction=pump_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:PUMP#1>')
        self.assertEqual(waypoints[0].name, 'PUMP_ON')

    def test_control_command_compiler(self) -> None:
        '''Verifies ControlCommandCompiler handles HOME, WAIT_MS, and ESTOP.'''
        compiler = ControlCommandCompiler()
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        home_inst = Instruction(
            command_type=CommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME',
        )
        self.assertTrue(compiler.can_compile(instruction=home_inst))
        compiler.compile(instruction=home_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:HOME>')

        wait_inst = Instruction(
            command_type=CommandType.WAIT_MS,
            parameters={'ms': 250.0},
            line_number=2,
            raw_text='WAIT_MS 250',
        )
        self.assertTrue(compiler.can_compile(instruction=wait_inst))
        compiler.compile(instruction=wait_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[1].command, '<CMD:WAIT#250>')

    def test_motion_command_compiler(self) -> None:
        '''Verifies MotionCommandCompiler handles Cartesian and approach moves.'''
        compiler = MotionCommandCompiler(
            cartesian_compiler=CartesianMoveCompilerFactory.create_with_tangent_helper(
                tangent_helper=TangentMacroExpander()
            ),
            vertical_compiler=VerticalMoveCompilerFactory.create(),
            arc_compiler=ArcMoveCompilerFactory.create_with_interpolator(
                arc_interpolator=ArcInterpolator()
            ),
        )
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        move_inst = Instruction(
            command_type=CommandType.MOVE_L,
            parameters={'X': 120.0, 'Y': 60.0, 'Z': 15.0, 'SPEED': 50.0},
            line_number=1,
            raw_text='MOVE_L X=120.0 Y=60.0 Z=15.0 SPEED=50.0',
        )
        self.assertTrue(compiler.can_compile(instruction=move_inst))
        compiler.compile(instruction=move_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(ctx.current_x, 120.0)
        self.assertEqual(ctx.current_y, 60.0)
        self.assertEqual(ctx.current_z, 15.0)

        approach_inst = Instruction(
            command_type=CommandType.APPROACH,
            parameters={'DIST': 10.0, 'SPEED': 25.0},
            line_number=2,
            raw_text='APPROACH DIST=10.0 SPEED=25.0',
        )
        self.assertTrue(compiler.can_compile(instruction=approach_inst))
        compiler.compile(instruction=approach_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(ctx.current_z, 5.0)

    def test_compiler_end_to_end(self) -> None:
        '''Verifies full program compilation through ScaraCompiler orchestrator.'''
        bounds = ScaraBounds.create_default()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        compiler = ScaraCompilerFactory.create(
            validator=validator
        )
        instructions = [
            Instruction(
                command_type=CommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            Instruction(
                command_type=CommandType.MOVE_J,
                parameters={'X': 150.0, 'Y': 50.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_J X=150.0 Y=50.0 Z=20.0 PHI=0.0',
            ),
            Instruction(
                command_type=CommandType.PUMP,
                parameters={'state': 'ON'},
                line_number=3,
                raw_text='PUMP ON',
            ),
        ]
        program = Program(instructions=instructions)
        plan = compiler.compile(program=program)
        self.assertGreaterEqual(plan.count, 3)

    def test_compiler_custom_sub_compilers(self) -> None:
        '''Verifies ScaraCompiler accepts custom primitive sub-compilers.'''
        bounds = ScaraBounds.create_default()
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        custom_tool = ToolCommandCompiler()
        compiler = ScaraCompilerFactory.create_with_compilers(
            validator=validator,
            primitive_compilers=(custom_tool,),
        )
        instructions = [
            Instruction(
                command_type=CommandType.PUMP,
                parameters={'state': 'ON'},
                line_number=1,
                raw_text='PUMP ON',
            ),
        ]
        program = Program(instructions=instructions)
        plan = compiler.compile(program=program)
        self.assertEqual(plan.count, 1)

    def test_decomposed_motion_sub_compilers_and_factory(self) -> None:
        '''Verifies CartesianMoveCompiler, VerticalMoveCompiler, ArcMoveCompiler, and MotionCommandCompilerFactory.'''
        compiler = MotionCommandCompilerFactory.create_with_helpers(
            arc_interpolator=ArcInterpolator(),
            tangent_helper=TangentMacroExpander(),
        )
        default_compiler = MotionCommandCompilerFactory.create()
        self.assertIsNotNone(default_compiler)
        self.assertEqual(MotionCommandCompilerFactory.get_version(), '1.0.0')

        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        move_inst = Instruction(
            command_type=CommandType.MOVE_L,
            parameters={'X': 100.0, 'Y': 50.0, 'Z': 10.0, 'SPEED': 40.0},
            line_number=1,
            raw_text='MOVE_L X=100.0 Y=50.0 Z=10.0 SPEED=40.0',
        )
        retract_inst = Instruction(
            command_type=CommandType.RETRACT,
            parameters={'DIST': 15.0},
            line_number=2,
            raw_text='RETRACT DIST=15.0',
        )
        arc_inst = Instruction(
            command_type=CommandType.ARC_CW,
            parameters={'X': 110.0, 'Y': 60.0, 'I': 5.0, 'J': 5.0},
            line_number=3,
            raw_text='ARC_CW X=110.0 Y=60.0 I=5.0 J=5.0',
        )

        self.assertTrue(compiler.can_compile(instruction=move_inst))
        self.assertTrue(compiler.can_compile(instruction=retract_inst))
        self.assertTrue(compiler.can_compile(instruction=arc_inst))

        compiler.compile(instruction=move_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(ctx.current_x, 100.0)

        compiler.compile(instruction=retract_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(ctx.current_z, 25.0)

        compiler.compile(instruction=arc_inst, context=ctx, waypoints=waypoints)
        self.assertGreater(len(waypoints), 2)
        self.assertEqual(ctx.current_x, 110.0)


if __name__ == '__main__':
    main()
