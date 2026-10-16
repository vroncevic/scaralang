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
    Unit tests for VerticalMoveCompiler component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.primitive.motion.isub_compiler import IMotionSubCompiler
from scaralang.core.service.compiler.primitive.motion.vertical.compiler import VerticalMoveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVerticalMoveCompiler(TestCase):
    '''
        Test cases verifying VerticalMoveCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixture.
                | test_protocol_conformance - Verifies IMotionSubCompiler conformance.
                | test_get_version - Verifies get_version returns valid version string.
                | test_can_compile - Verifies handled command types.
                | test_compile_approach_default - Verifies approach compilation with defaults.
                | test_compile_approach_with_speed - Verifies approach with explicit speed.
                | test_compile_approach_clamp_zero - Verifies approach clamping z to zero.
                | test_compile_retract_default - Verifies retract compilation with defaults.
                | test_compile_retract_with_speed - Verifies retract with explicit speed.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.compiler = VerticalMoveCompiler()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMotionSubCompiler protocol.
        '''
        self.assertIsInstance(self.compiler, IMotionSubCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.compiler.get_version(), '1.0.9')

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies APPROACH and RETRACT instructions.
        '''
        approach_inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={ScaraInstructionParam.DIST: 15.0},
            line_number=1,
            raw_text='APPROACH 15.0',
        )
        retract_inst = ScaraInstruction(
            command_type=ScaraCommandType.RETRACT,
            parameters={ScaraInstructionParam.DIST: 20.0},
            line_number=2,
            raw_text='RETRACT 20.0',
        )
        move_l_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={ScaraInstructionParam.X: 50.0},
            line_number=3,
            raw_text='MOVE_L X=50.0',
        )
        self.assertTrue(self.compiler.can_compile(instruction=approach_inst))
        self.assertTrue(self.compiler.can_compile(instruction=retract_inst))
        self.assertFalse(self.compiler.can_compile(instruction=move_l_inst))

    def test_compile_approach_default(self) -> None:
        '''
            Verifies compile generates valid Waypoint for APPROACH with default speed.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_x = 100.0
        context.pose.current_y = 50.0
        context.pose.current_z = 30.0
        context.pose.current_phi = 15.0
        context.speed.speed_work = 25.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={ScaraInstructionParam.DIST: 10.0},
            line_number=1,
            raw_text='APPROACH 10.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        wp = waypoints[0]
        self.assertEqual(wp.x, 100.0)
        self.assertEqual(wp.y, 50.0)
        self.assertEqual(wp.z, 20.0)
        self.assertEqual(wp.phi, 15.0)
        self.assertEqual(wp.speed, 25.0)
        self.assertEqual(wp.name, ScaraCommandType.APPROACH.value)
        self.assertEqual(context.pose.current_z, 20.0)

    def test_compile_approach_with_speed(self) -> None:
        '''
            Verifies compile handles explicit speed in APPROACH instruction.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_z = 25.0
        inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={
                ScaraInstructionParam.DIST: 5.0,
                ScaraInstructionParam.SPEED: 40.0,
            },
            line_number=1,
            raw_text='APPROACH 5.0 SPEED=40.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].z, 20.0)
        self.assertEqual(waypoints[0].speed, 40.0)
        self.assertEqual(context.pose.current_z, 20.0)

    def test_compile_approach_clamp_zero(self) -> None:
        '''
            Verifies compile clamps z coordinate to zero on excessive approach distance.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_z = 5.0
        inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={ScaraInstructionParam.DIST: 20.0},
            line_number=1,
            raw_text='APPROACH 20.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].z, 0.0)
        self.assertEqual(context.pose.current_z, 0.0)

    def test_compile_retract_default(self) -> None:
        '''
            Verifies compile generates valid Waypoint for RETRACT with rapid speed.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_x = 80.0
        context.pose.current_y = 40.0
        context.pose.current_z = 10.0
        context.pose.current_phi = 0.0
        context.speed.speed_rapid = 100.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.RETRACT,
            parameters={ScaraInstructionParam.DIST: 15.0},
            line_number=1,
            raw_text='RETRACT 15.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        wp = waypoints[0]
        self.assertEqual(wp.x, 80.0)
        self.assertEqual(wp.y, 40.0)
        self.assertEqual(wp.z, 25.0)
        self.assertEqual(wp.phi, 0.0)
        self.assertEqual(wp.speed, 100.0)
        self.assertEqual(wp.name, ScaraCommandType.RETRACT.value)
        self.assertEqual(context.pose.current_z, 25.0)

    def test_compile_retract_with_speed(self) -> None:
        '''
            Verifies compile handles explicit speed in RETRACT instruction.
        '''
        context = CompilerContextFactory.create()
        context.pose.current_z = 10.0
        inst = ScaraInstruction(
            command_type=ScaraCommandType.RETRACT,
            parameters={
                ScaraInstructionParam.DIST: 10.0,
                ScaraInstructionParam.SPEED: 75.0,
            },
            line_number=1,
            raw_text='RETRACT 10.0 SPEED=75.0',
        )
        waypoints = self.compiler.compile(instruction=inst, context=context)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].z, 20.0)
        self.assertEqual(waypoints[0].speed, 75.0)
        self.assertEqual(context.pose.current_z, 20.0)


if __name__ == '__main__':
    main()
