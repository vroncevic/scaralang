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
    Unit tests for PalletMacroExpander.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.macro.frame import WorkFrame
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.service.compiler.context.factory import CompilerContextFactory
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.pallet.dependencies import PalletDependencies
from scaralang.core.service.compiler.macro.pallet.expander import PalletMacroExpander
from scaralang.core.service.transformation.factory import TransformationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPalletMacroExpander(TestCase):
    '''
        Test cases verifying PalletMacroExpander behavior.

        It defines:

            :methods:
                | setUp - Prepares expander instance with dependencies.
                | test_protocol_conformance - Verifies IMacroExpander conformance.
                | test_can_expand - Verifies handling of pallet instructions.
                | test_expand_pallet_def - Verifies pallet definition registration.
                | test_expand_move_pallet - Verifies expanding MOVE_PALLET into MOVE_L.
                | test_expand_move_pallet_undefined - Verifies error on undefined pallet.
                | test_expand_pallet_def_invalid_dimensions - Verifies error on non-positive rows or cols.
                | test_expand_move_pallet_out_of_bounds - Verifies error on out-of-bounds cell index.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with frame transformer.
        '''
        self.transformer = TransformationFactory.create().transformer
        self.deps = PalletDependencies(frame_transformer=self.transformer)
        self.expander = PalletMacroExpander(dependencies=self.deps)

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
            parameters={
                ScaraInstructionParam.NAME: 'BOX',
                ScaraInstructionParam.ROWS: 2,
                ScaraInstructionParam.COLS: 2,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=BOX ROWS=2 COLS=2',
        )
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={
                ScaraInstructionParam.NAME: 'BOX',
                ScaraInstructionParam.INDEX: 0,
            },
            line_number=2,
            raw_text='MOVE_PALLET NAME=BOX INDEX=0',
        )
        other_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={
                ScaraInstructionParam.X: 100.0,
                ScaraInstructionParam.Y: 50.0,
            },
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
        context = CompilerContextFactory.create()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                ScaraInstructionParam.NAME: 'TRAY',
                ScaraInstructionParam.ROWS: 3,
                ScaraInstructionParam.COLS: 4,
                ScaraInstructionParam.DX: 15.0,
                ScaraInstructionParam.DY: 20.0,
                ScaraInstructionParam.START_X: 50.0,
                ScaraInstructionParam.START_Y: 60.0,
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
        context = CompilerContextFactory.create()
        def_inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                ScaraInstructionParam.NAME: 'GRID',
                ScaraInstructionParam.ROWS: 2,
                ScaraInstructionParam.COLS: 2,
                ScaraInstructionParam.DX: 10.0,
                ScaraInstructionParam.DY: 10.0,
                ScaraInstructionParam.START_X: 100.0,
                ScaraInstructionParam.START_Y: 100.0,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=GRID ROWS=2 COLS=2 DX=10.0 DY=10.0 START_X=100.0 START_Y=100.0',
        )
        self.expander.expand(instruction=def_inst, context=context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={
                ScaraInstructionParam.NAME: 'GRID',
                ScaraInstructionParam.INDEX: 3,
                ScaraInstructionParam.Z: 15.0,
            },
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

    def test_expand_move_pallet_with_3d_frame(self) -> None:
        '''
            Verifies MOVE_PALLET incorporates 3D work frame origin into target pose.
        '''
        context = CompilerContextFactory.create()
        context.active_frame = WorkFrame(
            origin=Point3D(x=50.0, y=50.0, z=10.0),
            angle_deg=0.0,
        )
        def_inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                ScaraInstructionParam.NAME: 'BOX',
                ScaraInstructionParam.ROWS: 1,
                ScaraInstructionParam.COLS: 2,
                ScaraInstructionParam.DX: 20.0,
                ScaraInstructionParam.DY: 20.0,
                ScaraInstructionParam.START_X: 0.0,
                ScaraInstructionParam.START_Y: 0.0,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=BOX ROWS=1 COLS=2 DX=20.0 DY=20.0 START_X=0.0 START_Y=0.0',
        )
        self.expander.expand(instruction=def_inst, context=context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={
                ScaraInstructionParam.NAME: 'BOX',
                ScaraInstructionParam.INDEX: 1,
                ScaraInstructionParam.Z: 5.0,
            },
            line_number=2,
            raw_text='MOVE_PALLET NAME=BOX INDEX=1 Z=5.0',
        )
        result = self.expander.expand(instruction=move_inst, context=context)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(context.pose.current_x, 70.0)
        self.assertAlmostEqual(context.pose.current_y, 50.0)
        self.assertAlmostEqual(context.pose.current_z, 15.0)

    def test_expand_move_pallet_undefined(self) -> None:
        '''
            Verifies ScaraSemanticError is raised when MOVE_PALLET references unknown pallet.
        '''
        context = CompilerContextFactory.create()
        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={
                ScaraInstructionParam.NAME: 'UNKNOWN',
                ScaraInstructionParam.INDEX: 0,
            },
            line_number=5,
            raw_text='MOVE_PALLET NAME=UNKNOWN INDEX=0',
        )
        with self.assertRaises(ScaraSemanticError):
            self.expander.expand(instruction=move_inst, context=context)

    def test_expand_pallet_def_invalid_dimensions(self) -> None:
        '''
            Verifies ScaraSemanticError is raised when rows or cols are non-positive.
        '''
        context = CompilerContextFactory.create()
        inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                ScaraInstructionParam.NAME: 'BAD',
                ScaraInstructionParam.ROWS: 0,
                ScaraInstructionParam.COLS: 2,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=BAD ROWS=0 COLS=2',
        )
        with self.assertRaises(ScaraSemanticError):
            self.expander.expand(instruction=inst, context=context)

    def test_expand_move_pallet_out_of_bounds(self) -> None:
        '''
            Verifies ScaraSemanticError is raised when cell index is out of bounds.
        '''
        context = CompilerContextFactory.create()
        def_inst = ScaraInstruction(
            command_type=ScaraCommandType.PALLET_DEF,
            parameters={
                ScaraInstructionParam.NAME: 'GRID',
                ScaraInstructionParam.ROWS: 2,
                ScaraInstructionParam.COLS: 2,
            },
            line_number=1,
            raw_text='PALLET_DEF NAME=GRID ROWS=2 COLS=2',
        )
        self.expander.expand(instruction=def_inst, context=context)

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_PALLET,
            parameters={
                ScaraInstructionParam.NAME: 'GRID',
                ScaraInstructionParam.INDEX: 4,
            },
            line_number=2,
            raw_text='MOVE_PALLET NAME=GRID INDEX=4',
        )
        with self.assertRaises(ScaraSemanticError):
            self.expander.expand(instruction=move_inst, context=context)


if __name__ == '__main__':
    main()
