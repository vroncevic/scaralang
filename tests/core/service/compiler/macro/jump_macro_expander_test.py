# -*- coding: UTF-8 -*-

'''
Module
    jump_macro_expander_test.py
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
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander
from scaralang.core.service.compiler.macro.jump_macro_expander import JumpMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
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
                | test_expand_jump - Verifies 3-phase expansion of JUMP instruction.
                | test_expand_jump_with_arch_height - Verifies ARCH_HEIGHT parameter handling.
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
                InstructionParam.X: 120.0,
                InstructionParam.Y: 80.0,
                InstructionParam.Z: 10.0,
            },
            line_number=1,
            raw_text='JUMP X=120.0 Y=80.0 Z=10.0',
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
            Verifies JUMP expands into lift, transit, and descent instructions.
        '''
        context = ScaraCompilerContext()
        context.current_x = 10.0
        context.current_y = 20.0
        context.current_z = 5.0
        context.current_phi = 0.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 150.0,
                InstructionParam.Z: 2.0,
                InstructionParam.PHI: 30.0,
                InstructionParam.SPEED: 50.0,
            },
            line_number=1,
            raw_text='JUMP X=100.0 Y=150.0 Z=2.0 PHI=30.0 SPEED=50.0',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(len(result), 3)

        lift_inst, transit_inst, descend_inst = result
        self.assertEqual(lift_inst.command_type, ScaraCommandType.MOVE_L)
        self.assertEqual(transit_inst.command_type, ScaraCommandType.MOVE_J)
        self.assertEqual(descend_inst.command_type, ScaraCommandType.MOVE_L)

        # Default arch is 20.0; clearance = max(5.0, 2.0) + 20.0 = 25.0
        self.assertEqual(lift_inst.parameters[InstructionParam.Z], 25.0)
        self.assertEqual(transit_inst.parameters[InstructionParam.X], 100.0)
        self.assertEqual(transit_inst.parameters[InstructionParam.Y], 150.0)
        self.assertEqual(transit_inst.parameters[InstructionParam.Z], 25.0)
        self.assertEqual(descend_inst.parameters[InstructionParam.Z], 2.0)

        # Context updated to final destination
        self.assertEqual(context.current_x, 100.0)
        self.assertEqual(context.current_y, 150.0)
        self.assertEqual(context.current_z, 2.0)
        self.assertEqual(context.current_phi, 30.0)

    def test_expand_jump_with_arch_height(self) -> None:
        '''
            Verifies custom ARCH_HEIGHT parameter sets correct clearance.
        '''
        context = ScaraCompilerContext()
        context.current_x = 0.0
        context.current_y = 0.0
        context.current_z = 10.0

        inst = ScaraInstruction(
            command_type=ScaraCommandType.JUMP,
            parameters={
                InstructionParam.X: 50.0,
                InstructionParam.Y: 50.0,
                InstructionParam.Z: 15.0,
                InstructionParam.ARCH_HEIGHT: 35.0,
            },
            line_number=1,
            raw_text='JUMP X=50.0 Y=50.0 Z=15.0 ARCH_HEIGHT=35.0',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(len(result), 3)
        # max(10.0, 15.0) + 35.0 = 50.0
        self.assertEqual(result[0].parameters[InstructionParam.Z], 50.0)


if __name__ == '__main__':
    main()
