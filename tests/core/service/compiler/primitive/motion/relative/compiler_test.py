# -*- coding: UTF-8 -*-

'''
Module
    compiler_test.py
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
    Unit tests for RelativeMoveCompiler component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.model.dsl.macro.frame import WorkFrame
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.primitive.motion.cartesian.tangent_heading_calculator_factory import TangentHeadingCalculatorFactory
from scaralang.core.service.compiler.primitive.motion.isub_compiler import IMotionSubCompiler
from scaralang.core.service.compiler.primitive.motion.relative.compiler import RelativeMoveCompiler
from scaralang.core.service.transformation.factory import TransformationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestRelativeMoveCompiler(TestCase):
    '''
        Test cases verifying RelativeMoveCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixture.
                | test_protocol_conformance - Verifies IMotionSubCompiler conformance.
                | test_get_version - Verifies get_version returns valid version string.
                | test_can_compile - Verifies handled command types.
                | test_compile_move_rel - Verifies relative motion waypoint compilation.
                | test_compile_tangential_and_frame - Verifies tangential mode and work frame.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.

            :exceptions: None.
        '''
        self.compiler = RelativeMoveCompiler(
            tangent_calculator=TangentHeadingCalculatorFactory.create(),
            frame_transformer=TransformationFactory.create().transformer,
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMotionSubCompiler protocol.

            :exceptions: None.
        '''
        self.assertIsInstance(self.compiler, IMotionSubCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.

            :exceptions: None.
        '''
        self.assertEqual(self.compiler.get_version(), '1.1.1')

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies MOVE_REL instructions.

            :exceptions: None.
        '''
        rel_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_REL,
            parameters={ScaraInstructionParam.X: 10.0, ScaraInstructionParam.Y: 20.0},
            line_number=1,
            raw_text='MOVE_REL X=10.0 Y=20.0',
        )
        other_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={ScaraInstructionParam.X: 10.0},
            line_number=2,
            raw_text='MOVE_L X=10.0',
        )
        self.assertTrue(self.compiler.can_compile(instruction=rel_inst))
        self.assertFalse(self.compiler.can_compile(instruction=other_inst))

    def test_compile_move_rel(self) -> None:
        '''
            Verifies compile generates valid Waypoint for MOVE_REL and updates pose.

            :exceptions: None.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_x = 50.0
        context.pose.current_y = 50.0
        context.pose.current_z = 10.0
        context.pose.current_phi = 0.0

        inst1 = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_REL,
            parameters={
                ScaraInstructionParam.X: 20.0,
                ScaraInstructionParam.Y: -10.0,
                ScaraInstructionParam.Z: 5.0,
                ScaraInstructionParam.PHI: 30.0,
                ScaraInstructionParam.SPEED: 80.0,
            },
            line_number=1,
            raw_text='MOVE_REL X=20.0 Y=-10.0 Z=5.0 PHI=30.0 SPEED=80.0',
        )
        waypoints1 = self.compiler.compile(instruction=inst1, context=context)
        self.assertEqual(len(waypoints1), 1)
        wp1 = waypoints1[0]
        self.assertAlmostEqual(wp1.x, 70.0)
        self.assertAlmostEqual(wp1.y, 40.0)
        self.assertAlmostEqual(wp1.z, 15.0)
        self.assertAlmostEqual(wp1.phi, 30.0)
        self.assertAlmostEqual(wp1.speed, 80.0)
        self.assertAlmostEqual(context.pose.current_x, 70.0)
        self.assertAlmostEqual(context.pose.current_y, 40.0)
        self.assertAlmostEqual(context.pose.current_z, 15.0)
        self.assertAlmostEqual(context.pose.current_phi, 30.0)

        inst2 = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_REL,
            parameters={ScaraInstructionParam.X: -30.0, ScaraInstructionParam.Y: 10.0},
            line_number=2,
            raw_text='MOVE_REL X=-30.0 Y=10.0',
        )
        waypoints2 = self.compiler.compile(instruction=inst2, context=context)
        self.assertEqual(len(waypoints2), 1)
        wp2 = waypoints2[0]
        self.assertAlmostEqual(wp2.x, 40.0)
        self.assertAlmostEqual(wp2.y, 50.0)
        self.assertAlmostEqual(wp2.z, 15.0)
        self.assertAlmostEqual(wp2.phi, 30.0)

    def test_compile_tangential_and_frame(self) -> None:
        '''
            Verifies tangential orientation and active frame handling during relative motion.

            :exceptions: None.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_x = 100.0
        context.pose.current_y = 100.0
        context.pose.current_z = 20.0
        context.active_frame = WorkFrame(
            origin=Point3D(x=100.0, y=100.0, z=20.0),
            angle_deg=0.0,
        )
        context.tool_orient_mode = ToolOrientMode.TANGENTIAL

        inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_REL,
            parameters={ScaraInstructionParam.X: 30.0, ScaraInstructionParam.Y: 30.0},
            line_number=1,
            raw_text='MOVE_REL X=30.0 Y=30.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        wp = waypoints[0]
        self.assertAlmostEqual(wp.x, 130.0)
        self.assertAlmostEqual(wp.y, 130.0)
        self.assertAlmostEqual(wp.z, 20.0)
        self.assertAlmostEqual(wp.phi, 45.0, places=3)


if __name__ == '__main__':
    main()
