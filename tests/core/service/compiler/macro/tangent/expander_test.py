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
    Unit tests for TangentMacroExpander.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.ast.tool_orient_mode import ToolOrientMode
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.tangent.expander import TangentMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTangentMacroExpander(TestCase):
    '''
        Test cases verifying TangentMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares expander instance.
                | test_protocol_conformance - Verifies IMacroExpander conformance.
                | test_can_expand - Verifies handling of TOOL_ORIENT instructions.
                | test_expand_tangential - Verifies configuring TANGENTIAL mode.
                | test_expand_with_phi - Verifies updating explicit phi.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.expander = TangentMacroExpander()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMacroExpander protocol.
        '''
        self.assertIsInstance(self.expander, IMacroExpander)

    def test_can_expand(self) -> None:
        '''
            Verifies can_expand identifies TOOL_ORIENT instructions.
        '''
        tool_orient_inst = ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            parameters={ScaraInstructionParam.MODE: ToolOrientMode.TANGENTIAL},
            line_number=1,
            raw_text='TOOL_ORIENT TANGENTIAL',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={
                ScaraInstructionParam.X: 100.0,
                ScaraInstructionParam.Y: 50.0,
            },
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=50.0',
        )
        self.assertTrue(self.expander.can_expand(instruction=tool_orient_inst))
        self.assertFalse(self.expander.can_expand(instruction=move_inst))

    def test_expand_tangential(self) -> None:
        '''
            Verifies expand sets TANGENTIAL tool orient mode in context.
        '''
        context = CompilerContextFactory.create()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            parameters={ScaraInstructionParam.MODE: ToolOrientMode.TANGENTIAL},
            line_number=1,
            raw_text='TOOL_ORIENT TANGENTIAL',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(result, ())
        self.assertEqual(context.tool_orient_mode, ToolOrientMode.TANGENTIAL)

    def test_expand_with_phi(self) -> None:
        '''
            Verifies expand updates current_phi when phi parameter is provided.
        '''
        context = CompilerContextFactory.create()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.TOOL_ORIENT,
            parameters={
                ScaraInstructionParam.MODE: ToolOrientMode.FIXED,
                ScaraInstructionParam.PHI: 45.0,
            },
            line_number=1,
            raw_text='TOOL_ORIENT FIXED PHI=45.0',
        )
        self.expander.expand(instruction=inst, context=context)
        self.assertEqual(context.tool_orient_mode, ToolOrientMode.FIXED)
        self.assertEqual(context.pose.current_phi, 45.0)


if __name__ == '__main__':
    main()
