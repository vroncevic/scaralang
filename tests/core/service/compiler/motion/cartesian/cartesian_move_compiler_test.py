# -*- coding: UTF-8 -*-

'''
Module
    cartesian_move_compiler_test.py
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
    Unit tests for CartesianMoveCompiler component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.frame.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.compiler.macro.tangent_macro_expander_factory import TangentMacroExpanderFactory
from scaralang.core.service.compiler.motion.cartesian.cartesian_move_compiler import CartesianMoveCompiler
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCartesianMoveCompiler(TestCase):
    '''
        Test cases verifying CartesianMoveCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixture.
                | test_protocol_conformance - Verifies IMotionSubCompiler conformance.
                | test_can_compile - Verifies handled command types.
                | test_compile_move_l - Verifies linear motion waypoint compilation.
                | test_compile_move_j - Verifies joint motion waypoint compilation.
                | test_compile_tangential_orientation - Verifies tangential tool orientation mode.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.compiler = CartesianMoveCompiler(
            tangent_helper=TangentMacroExpanderFactory.create(),
            frame_transformer=FrameTransformerFactory.create(),
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMotionSubCompiler protocol.
        '''
        self.assertIsInstance(self.compiler, IMotionSubCompiler)

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies MOVE_L and MOVE_J instructions.
        '''
        move_l_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={InstructionParam.X: 100.0, InstructionParam.Y: 50.0},
            line_number=1,
            raw_text='MOVE_L X=100.0 Y=50.0',
        )
        move_j_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            parameters={InstructionParam.X: 50.0, InstructionParam.Y: 25.0},
            line_number=2,
            raw_text='MOVE_J X=50.0 Y=25.0',
        )
        other_inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={InstructionParam.DIST: 10.0},
            line_number=3,
            raw_text='APPROACH 10.0',
        )
        self.assertTrue(self.compiler.can_compile(instruction=move_l_inst))
        self.assertTrue(self.compiler.can_compile(instruction=move_j_inst))
        self.assertFalse(self.compiler.can_compile(instruction=other_inst))

    def test_compile_move_l(self) -> None:
        '''
            Verifies compile generates valid Waypoint for MOVE_L.
        '''
        context = ScaraCompilerContext()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={
                InstructionParam.X: 120.0,
                InstructionParam.Y: 80.0,
                InstructionParam.Z: 15.0,
                InstructionParam.PHI: 45.0,
                InstructionParam.SPEED: 60.0,
            },
            line_number=1,
            raw_text='MOVE_L X=120.0 Y=80.0 Z=15.0 PHI=45.0 SPEED=60.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        wp = waypoints[0]
        self.assertEqual(wp.x, 120.0)
        self.assertEqual(wp.y, 80.0)
        self.assertEqual(wp.z, 15.0)
        self.assertEqual(wp.phi, 45.0)
        self.assertEqual(context.current_x, 120.0)
        self.assertEqual(context.current_y, 80.0)

    def test_compile_move_j(self) -> None:
        '''
            Verifies compile generates valid Waypoint for MOVE_J.
        '''
        context = ScaraCompilerContext()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            parameters={
                InstructionParam.X: 50.0,
                InstructionParam.Y: 20.0,
            },
            line_number=1,
            raw_text='MOVE_J X=50.0 Y=20.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].x, 50.0)
        self.assertEqual(waypoints[0].y, 20.0)

    def test_compile_tangential_orientation(self) -> None:
        '''
            Verifies tool orientation follows motion tangent in TANGENTIAL mode.
        '''
        context = ScaraCompilerContext()
        context.current_x = 0.0
        context.current_y = 0.0
        context.tool_orient_mode = ToolOrientMode.TANGENTIAL

        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={
                InstructionParam.X: 50.0,
                InstructionParam.Y: 50.0,
            },
            line_number=1,
            raw_text='MOVE_L X=50.0 Y=50.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        self.assertAlmostEqual(waypoints[0].phi, 45.0, places=3)


if __name__ == '__main__':
    main()
