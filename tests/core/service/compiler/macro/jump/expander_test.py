# -*- coding: UTF-8 -*-

'''
Module
    expander_test.py
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
    Unit tests for JumpMacroExpander.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.jump.expander import JumpMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJumpMacroExpander(TestCase):
    '''
        Test cases verifying JumpMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares expander instance.
                | test_protocol_conformance - Verifies IMacroExpander conformance.
                | test_can_expand - Verifies handling of JUMP instructions.
                | test_expand_jump - Verifies 3-phase clearance expansion and context updates.
                | test_expand_jump_with_defaults - Verifies default parameter handling.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.expander = JumpMacroExpander()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMacroExpander protocol.
        '''
        self.assertIsInstance(self.expander, IMacroExpander)

    def test_can_expand(self) -> None:
        '''
            Verifies can_expand identifies JUMP instructions.
        '''
        jump_inst = ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 10.0,
            },
            line_number=1,
            raw_text='JUMP X=100.0 Y=50.0 Z=10.0',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={InstructionParam.X: 100.0, InstructionParam.Y: 50.0},
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=50.0',
        )
        self.assertTrue(self.expander.can_expand(instruction=jump_inst))
        self.assertFalse(self.expander.can_expand(instruction=move_inst))

    def test_expand_jump(self) -> None:
        '''
            Verifies JUMP expands to 3 instructions (Lift, Transit, Descent) and updates pose.
        '''
        context = ScaraCompilerContext()
        context.pose.current_x = 10.0
        context.pose.current_y = 20.0
        context.pose.current_z = 5.0
        context.pose.current_phi = 0.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 200.0,
                InstructionParam.Z: 15.0,
                InstructionParam.PHI: 45.0,
                InstructionParam.ARCH_HEIGHT: 25.0,
                InstructionParam.SPEED: 150.0,
            },
            line_number=5,
            raw_text='JUMP X=100.0 Y=200.0 Z=15.0 PHI=45.0 ARCH=25.0 SPEED=150.0',
        )

        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(len(result), 3)

        lift, transit, descend = result

        # Lift: Z = max(5.0, 15.0) + 25.0 = 40.0
        self.assertEqual(lift.command_type, ScaraCommandType.MOVE_L)
        self.assertEqual(lift.parameters[InstructionParam.X], 10.0)
        self.assertEqual(lift.parameters[InstructionParam.Y], 20.0)
        self.assertEqual(lift.parameters[InstructionParam.Z], 40.0)
        self.assertEqual(lift.parameters[InstructionParam.SPEED], 150.0)

        # Transit: Move to target X, Y at clearance Z
        self.assertEqual(transit.command_type, ScaraCommandType.MOVE_J)
        self.assertEqual(transit.parameters[InstructionParam.X], 100.0)
        self.assertEqual(transit.parameters[InstructionParam.Y], 200.0)
        self.assertEqual(transit.parameters[InstructionParam.Z], 40.0)
        self.assertEqual(transit.parameters[InstructionParam.PHI], 45.0)

        # Descent: Move to target Z
        self.assertEqual(descend.command_type, ScaraCommandType.MOVE_L)
        self.assertEqual(descend.parameters[InstructionParam.X], 100.0)
        self.assertEqual(descend.parameters[InstructionParam.Y], 200.0)
        self.assertEqual(descend.parameters[InstructionParam.Z], 15.0)
        self.assertEqual(descend.parameters[InstructionParam.PHI], 45.0)

        # Context pose updated to final target
        self.assertEqual(context.pose.current_x, 100.0)
        self.assertEqual(context.pose.current_y, 200.0)
        self.assertEqual(context.pose.current_z, 15.0)
        self.assertEqual(context.pose.current_phi, 45.0)

    def test_expand_jump_with_defaults(self) -> None:
        '''
            Verifies JUMP uses context pose defaults when optional parameters are omitted.
        '''
        context = ScaraCompilerContext()
        context.pose.current_x = 30.0
        context.pose.current_y = 40.0
        context.pose.current_z = 0.0
        context.pose.current_phi = 10.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            parameters={},
            line_number=1,
            raw_text='JUMP',
        )

        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(len(result), 3)

        lift, _, descend = result
        # Default arch_height is 20.0, target_z default is 0.0 -> clearance_z = 20.0
        self.assertEqual(lift.parameters[InstructionParam.Z], 20.0)
        self.assertEqual(descend.parameters[InstructionParam.Z], 0.0)


if __name__ == '__main__':
    main()
