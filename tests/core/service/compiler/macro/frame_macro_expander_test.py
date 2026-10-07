# -*- coding: UTF-8 -*-

'''
Module
    frame_macro_expander_test.py
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
    Unit tests for FrameMacroExpander.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.compiler.macro.frame_macro_expander import FrameMacroExpander
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameMacroExpander(TestCase):
    '''
        Test cases verifying FrameMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares expander instance.
                | test_protocol_conformance - Verifies IMacroExpander conformance.
                | test_can_expand - Verifies handling of frame commands.
                | test_expand_frame_set - Verifies setting active work frame in context.
                | test_expand_frame_set_with_rz - Verifies setting frame using RZ parameter.
                | test_expand_frame_reset - Verifies resetting active frame in context.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.expander = FrameMacroExpander()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMacroExpander protocol.
        '''
        self.assertIsInstance(self.expander, IMacroExpander)

    def test_can_expand(self) -> None:
        '''
            Verifies can_expand identifies FRAME_SET and FRAME_RESET instructions.
        '''
        set_inst = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_SET,
            parameters={
                InstructionParam.X: 50.0,
                InstructionParam.Y: 30.0,
                InstructionParam.ANGLE: 45.0,
            },
            line_number=1,
            raw_text='FRAME_SET X=50.0 Y=30.0 ANGLE=45.0',
        )
        reset_inst = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_RESET,
            parameters={},
            line_number=2,
            raw_text='FRAME_RESET',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={InstructionParam.X: 100.0, InstructionParam.Y: 50.0},
            line_number=3,
            raw_text='MOVE_L X=100.0 Y=50.0',
        )
        self.assertTrue(self.expander.can_expand(instruction=set_inst))
        self.assertTrue(self.expander.can_expand(instruction=reset_inst))
        self.assertFalse(self.expander.can_expand(instruction=move_inst))

    def test_expand_frame_set(self) -> None:
        '''
            Verifies FRAME_SET updates context active_frame with X, Y, and ANGLE.
        '''
        context = ScaraCompilerContext()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_SET,
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 50.0,
                InstructionParam.ANGLE: 30.0,
            },
            line_number=1,
            raw_text='FRAME_SET X=100.0 Y=50.0 ANGLE=30.0',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(result, ())
        self.assertEqual(context.active_frame.origin.x, 100.0)
        self.assertEqual(context.active_frame.origin.y, 50.0)
        self.assertEqual(context.active_frame.angle_deg, 30.0)

    def test_expand_frame_set_with_rz(self) -> None:
        '''
            Verifies FRAME_SET updates context active_frame using RZ parameter.
        '''
        context = ScaraCompilerContext()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_SET,
            parameters={
                InstructionParam.X: 75.0,
                InstructionParam.Y: 25.0,
                InstructionParam.RZ: -15.0,
            },
            line_number=1,
            raw_text='FRAME_SET X=75.0 Y=25.0 RZ=-15.0',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(result, ())
        self.assertEqual(context.active_frame.origin.x, 75.0)
        self.assertEqual(context.active_frame.origin.y, 25.0)
        self.assertEqual(context.active_frame.angle_deg, -15.0)

    def test_expand_frame_reset(self) -> None:
        '''
            Verifies FRAME_RESET resets context active_frame to origin.
        '''
        context = ScaraCompilerContext()
        inst_set = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_SET,
            parameters={
                InstructionParam.X: 100.0,
                InstructionParam.Y: 50.0,
                InstructionParam.ANGLE: 30.0,
            },
            line_number=1,
            raw_text='FRAME_SET X=100.0 Y=50.0 ANGLE=30.0',
        )
        self.expander.expand(instruction=inst_set, context=context)
        self.assertNotEqual(context.active_frame.origin.x, 0.0)

        inst_reset = ScaraInstruction(
            command_type=ScaraCommandType.FRAME_RESET,
            parameters={},
            line_number=2,
            raw_text='FRAME_RESET',
        )
        result = self.expander.expand(instruction=inst_reset, context=context)
        self.assertEqual(result, ())
        self.assertEqual(context.active_frame.origin.x, 0.0)
        self.assertEqual(context.active_frame.origin.y, 0.0)
        self.assertEqual(context.active_frame.angle_deg, 0.0)


if __name__ == '__main__':
    main()
