# -*- coding: UTF-8 -*-

'''
Module
    state_command_compiler_test.py
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
    Unit tests for StateCommandCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.elbow_config import ElbowConfig
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.state.state_command_compiler import StateCommandCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateCommandCompiler(TestCase):
    '''
        Test cases verifying StateCommandCompiler functionality.

        It defines:

            :methods:
                | setUp - Prepares test fixtures.
                | test_protocol_conformance - Verifies IPrimitiveCompiler conformance.
                | test_can_compile - Verifies supported command identification.
                | test_compile_speed - Verifies speed mode and value updates.
                | test_compile_accel - Verifies acceleration updates.
                | test_compile_override - Verifies speed override percentage updates.
                | test_compile_elbow - Verifies elbow kinematic configuration updates.
                | test_compile_zone - Verifies zone mode and radius updates.
                | test_compile_unsupported_no_op - Verifies unhandled commands are ignored.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with compiler and context.
        '''
        self.compiler = StateCommandCompiler()
        self.context = ScaraCompilerContext()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol conformance to IPrimitiveCompiler.
        '''
        self.assertIsInstance(self.compiler, IPrimitiveCompiler)

    def test_can_compile(self) -> None:
        '''
            Verifies can_compile identifies state configuration commands.
        '''
        supported = (
            ScaraCommandType.SPEED,
            ScaraCommandType.ACCEL,
            ScaraCommandType.OVERRIDE,
            ScaraCommandType.CONFIG_ELBOW,
            ScaraCommandType.ZONE,
        )
        for cmd in supported:
            inst = ScaraInstruction(command_type=cmd, parameters={}, line_number=1, raw_text='')
            self.assertTrue(self.compiler.can_compile(instruction=inst))

        unsupported = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='',
        )
        self.assertFalse(self.compiler.can_compile(instruction=unsupported))

    def test_compile_speed(self) -> None:
        '''
            Verifies SPEED instruction updates work and rapid speeds.
        '''
        work_inst = ScaraInstruction(
            command_type=ScaraCommandType.SPEED,
            parameters={
                InstructionParam.MODE: SpeedMode.WORK,
                InstructionParam.SPEED: 45.0,
            },
            line_number=1,
            raw_text='SPEED WORK 45.0',
        )
        result = self.compiler.compile(
            instruction=work_inst,
            context=self.context,
        )
        self.assertEqual(result, ())
        self.assertEqual(self.context.speed_work, 45.0)
        self.assertEqual(self.context.current_speed, 45.0)

        rapid_inst = ScaraInstruction(
            command_type=ScaraCommandType.SPEED,
            parameters={
                InstructionParam.MODE: SpeedMode.RAPID,
                InstructionParam.SPEED: 180.0,
            },
            line_number=2,
            raw_text='SPEED RAPID 180.0',
        )
        result_rapid = self.compiler.compile(
            instruction=rapid_inst,
            context=self.context,
        )
        self.assertEqual(result_rapid, ())
        self.assertEqual(self.context.speed_rapid, 180.0)

    def test_compile_accel(self) -> None:
        '''
            Verifies ACCEL instruction updates active acceleration.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.ACCEL,
            parameters={InstructionParam.ACCEL: 450.0},
            line_number=1,
            raw_text='ACCEL 450.0',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())
        self.assertEqual(self.context.active_accel, 450.0)

    def test_compile_override(self) -> None:
        '''
            Verifies OVERRIDE instruction updates speed override percentage.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.OVERRIDE,
            parameters={InstructionParam.PERCENT: 75.0},
            line_number=1,
            raw_text='OVERRIDE 75.0',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())
        self.assertEqual(self.context.speed_override_pct, 75.0)

    def test_compile_elbow(self) -> None:
        '''
            Verifies CONFIG_ELBOW instruction updates elbow configuration.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.CONFIG_ELBOW,
            parameters={InstructionParam.ELBOW: ElbowConfig.LEFT},
            line_number=1,
            raw_text='CONFIG_ELBOW LEFT',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())
        self.assertEqual(self.context.elbow_config, ElbowConfig.LEFT)

    def test_compile_zone(self) -> None:
        '''
            Verifies ZONE instruction updates zone mode and radius.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            parameters={
                InstructionParam.MODE: ZoneMode.BLEND,
                InstructionParam.RADIUS: 8.5,
            },
            line_number=1,
            raw_text='ZONE BLEND R=8.5',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())
        self.assertEqual(self.context.zone_mode, ZoneMode.BLEND)
        self.assertEqual(self.context.zone_radius, 8.5)

    def test_compile_unsupported_no_op(self) -> None:
        '''
            Verifies unsupported commands do not modify context or waypoints.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME',
        )
        result = self.compiler.compile(
            instruction=inst,
            context=self.context,
        )
        self.assertEqual(result, ())


if __name__ == '__main__':
    main()
