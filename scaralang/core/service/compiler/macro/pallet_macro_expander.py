# -*- coding: UTF-8 -*-

'''
Module
    pallet_macro_expander.py
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
    Implementation of IMacroExpander resolving pallet matrix definitions into discrete coordinates.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.service.compiler.frame.iframe_transformer import IFrameTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PalletMacroExpander:
    '''
        Macro expander managing pallet matrix layout definitions and calculating cell index targets.

        It defines:

            :attributes:
                | _frame_transformer - Coordinate frame transformer service.
            :methods:
                | __init__ - Initializes pallet macro expander with injected frame transformer.
                | can_expand - Checks if instruction is PALLET_DEF or MOVE_PALLET.
                | expand - Registers pallet or translates MOVE_PALLET into Cartesian motion.
    '''

    _frame_transformer: IFrameTransformer

    def __init__(
        self,
        *,
        frame_transformer: IFrameTransformer,
    ) -> None:
        '''
            Initializes PalletMacroExpander with injected frame transformer.

            :param frame_transformer: Injected IFrameTransformer instance.
            :exceptions: None.
        '''
        self._frame_transformer = frame_transformer

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks whether this expander handles pallet instructions.

            :param instruction: ScaraInstruction node to check.
            :return: True if PALLET_DEF or MOVE_PALLET, False otherwise.
        '''
        return instruction.command_type in (
            ScaraCommandType.PALLET_DEF,
            ScaraCommandType.MOVE_PALLET,
        )

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Processes PALLET_DEF or calculates cell coordinate for MOVE_PALLET.

            :param instruction: Pallet instruction node.
            :param context: Active compiler context.
            :return: Tuple of resulting instructions.
            :exceptions: KeyError if MOVE_PALLET references undefined pallet name.
        '''
        params = instruction.parameters
        name: str = str(params.get(InstructionParam.NAME, 'DEFAULT')).upper()

        if instruction.command_type == ScaraCommandType.PALLET_DEF:
            pallet_def = PalletDefinition(
                name=name,
                rows=int(params.get(InstructionParam.ROWS, 1)),
                cols=int(params.get(InstructionParam.COLS, 1)),
                dx=float(params.get(InstructionParam.DX, 20.0)),
                dy=float(params.get(InstructionParam.DY, 20.0)),
                start_x=float(params.get(InstructionParam.START_X, context.current_x)),
                start_y=float(params.get(InstructionParam.START_Y, context.current_y)),
            )
            context.pallets[name] = pallet_def
            return ()

        if name not in context.pallets:
            raise KeyError(
                f'Error at line {instruction.line_number}: '
                f'Pallet {name!r} is not defined before MOVE_PALLET'
            )

        pallet_def = context.pallets[name]
        index = int(params.get(InstructionParam.INDEX, 0))
        local_x = pallet_def.start_x + (index % pallet_def.cols) * pallet_def.dx
        local_y = pallet_def.start_y + (index // pallet_def.cols) * pallet_def.dy
        global_x, global_y = self._frame_transformer.transform_point(
            frame=context.active_frame,
            x=local_x,
            y=local_y,
        )
        target_z = float(params.get(InstructionParam.Z, context.current_z))

        context.current_x = global_x
        context.current_y = global_y
        context.current_z = target_z

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=instruction.line_number,
            raw_text=(
                f'# MOVE_PALLET: {name}[{index}] -> '
                f'X={global_x:.2f} Y={global_y:.2f} Z={target_z:.2f}'
            ),
            parameters={
                InstructionParam.X: global_x,
                InstructionParam.Y: global_y,
                InstructionParam.Z: target_z,
                InstructionParam.PHI: context.current_phi,
                InstructionParam.SPEED: context.current_speed,
            },
        )

        return (move_inst,)
