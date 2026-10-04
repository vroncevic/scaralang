# -*- coding: UTF-8 -*-

'''
Module
    pallet_macro_expander_test.py
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
    Unit tests for PalletMacroExpander.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.transformation.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.compiler.macro.imacro_expander import IMacroExpander
from scaralang.core.service.compiler.macro.pallet_macro_expander import PalletMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPalletMacroExpander(TestCase):
    '''
        Test cases verifying PalletMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares expander instance with transformer.
                | test_protocol_conformance - Verifies IMacroExpander conformance.
                | test_can_expand - Verifies handling of pallet instructions.
                | test_expand_pallet_def - Verifies pallet definition registration.
                | test_expand_move_pallet - Verifies expanding MOVE_PALLET into MOVE_L.
                | test_expand_move_pallet_undefined - Verifies error on undefined pallet.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with frame transformer.
        '''
        self.transformer = FrameTransformerFactory.create()
        self.expander = PalletMacroExpander(frame_transformer=self.transformer)

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to IMacroExpander protocol.
        '''
        self.assertIsInstance(self.expander, IMacroExpander)

    def test_can_expand(self) -> None:
        '''
            Verifies can_expand identifies PALLET_DEF and MOVE_PALLET instructions.
        '''
        def_inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={'NAME': 'BOX', 'ROWS': 2, 'COLS': 2},
            line_number=1,
            raw_text='PALLET_DEF NAME=BOX ROWS=2 COLS=2',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={'NAME': 'BOX', 'INDEX': 0},
            line_number=2,
            raw_text='MOVE_PALLET NAME=BOX INDEX=0',
        )
        other_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={'X': 100.0, 'Y': 50.0},
            line_number=3,
            raw_text='MOVE_L X=100.0 Y=50.0',
        )
        self.assertTrue(self.expander.can_expand(instruction=def_inst))
        self.assertTrue(self.expander.can_expand(instruction=move_inst))
        self.assertFalse(self.expander.can_expand(instruction=other_inst))

    def test_expand_pallet_def(self) -> None:
        '''
            Verifies PALLET_DEF registers PalletDefinition into context.
        '''
        context = ScaraCompilerContext()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                'NAME': 'TRAY',
                'ROWS': 3,
                'COLS': 4,
                'DX': 15.0,
                'DY': 20.0,
                'START_X': 50.0,
                'START_Y': 60.0,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=TRAY ROWS=3 COLS=4 DX=15.0 DY=20.0 START_X=50.0 START_Y=60.0',
        )
        result = self.expander.expand(instruction=inst, context=context)
        self.assertEqual(result, ())
        self.assertIn('TRAY', context.pallets)
        pallet = context.pallets['TRAY']
        self.assertEqual(pallet.rows, 3)
        self.assertEqual(pallet.cols, 4)

    def test_expand_move_pallet(self) -> None:
        '''
            Verifies MOVE_PALLET calculates grid coordinate and emits MOVE_L instruction.
        '''
        context = ScaraCompilerContext()
        def_inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                'NAME': 'GRID',
                'ROWS': 2,
                'COLS': 2,
                'DX': 10.0,
                'DY': 10.0,
                'START_X': 100.0,
                'START_Y': 100.0,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=GRID ROWS=2 COLS=2 DX=10.0 DY=10.0 START_X=100.0 START_Y=100.0',
        )
        self.expander.expand(instruction=def_inst, context=context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={'NAME': 'GRID', 'INDEX': 3, 'Z': 15.0},
            line_number=2,
            raw_text='MOVE_PALLET NAME=GRID INDEX=3 Z=15.0',
        )
        result = self.expander.expand(instruction=move_inst, context=context)
        self.assertEqual(len(result), 1)
        expanded = result[0]
        self.assertEqual(expanded.command_type, ScaraCommandType.MOVE_L)
        self.assertEqual(context.pose.current_x, 110.0)
        self.assertEqual(context.pose.current_y, 110.0)
        self.assertEqual(context.pose.current_z, 15.0)

    def test_expand_move_pallet_undefined(self) -> None:
        '''
            Verifies KeyError is raised when MOVE_PALLET references unknown pallet.
        '''
        context = ScaraCompilerContext()
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={'NAME': 'UNKNOWN', 'INDEX': 0},
            line_number=5,
            raw_text='MOVE_PALLET NAME=UNKNOWN INDEX=0',
        )
        with self.assertRaises(KeyError):
            self.expander.expand(instruction=move_inst, context=context)


if __name__ == '__main__':
    main()
