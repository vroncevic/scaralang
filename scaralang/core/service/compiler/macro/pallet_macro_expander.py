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

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.dsl.macro.pallet_definition import PalletDefinition
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.transformation.iframe_transformer import IFrameTransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
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
        self._frame_transformer: Final[IFrameTransformer] = frame_transformer

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
            :exceptions: ScaraSemanticError if PALLET_DEF has non-positive dimensions,
                         MOVE_PALLET references undefined pallet, or index is out of bounds.
        '''
        params = instruction.parameters
        name: str = str(params.get(InstructionParam.NAME, 'DEFAULT')).upper()

        if instruction.command_type == ScaraCommandType.PALLET_DEF:
            rows = int(params.get(InstructionParam.ROWS, 1))
            cols = int(params.get(InstructionParam.COLS, 1))

            if rows <= 0 or cols <= 0:
                raise ScaraSemanticError(
                    f'Error at line {instruction.line_number}: '
                    f'Pallet {name!r} rows and cols must be greater than zero, '
                    f'got rows={rows}, cols={cols}'
                )

            pallet_def = PalletDefinition(
                name=name,
                rows=rows,
                cols=cols,
                dx=float(params.get(InstructionParam.DX, 20.0)),
                dy=float(params.get(InstructionParam.DY, 20.0)),
                start=Point2D(
                    x=float(
                        params.get(InstructionParam.START_X, context.pose.current_x)
                    ),
                    y=float(
                        params.get(InstructionParam.START_Y, context.pose.current_y)
                    ),
                ),
            )
            context.pallets[name] = pallet_def

            return ()

        if name not in context.pallets:
            raise ScaraSemanticError(
                f'Error at line {instruction.line_number}: '
                f'Pallet {name!r} is not defined before MOVE_PALLET'
            )

        pallet_def = context.pallets[name]
        index = int(params.get(InstructionParam.INDEX, 0))
        max_cells: int = pallet_def.rows * pallet_def.cols

        if index < 0 or index >= max_cells:
            raise ScaraSemanticError(
                f'Error at line {instruction.line_number}: '
                f'Pallet index {index} out of bounds for pallet {name!r} '
                f'(capacity: {max_cells} cells, valid range: 0..{max_cells - 1})'
            )

        local_x = pallet_def.start.x + (index % pallet_def.cols) * pallet_def.dx
        local_y = pallet_def.start.y + (index // pallet_def.cols) * pallet_def.dy
        transformed_point = self._frame_transformer.transform_point(
            frame=context.active_frame,
            point=Point2D(x=local_x, y=local_y),
        )
        target_z = float(params.get(InstructionParam.Z, context.pose.current_z))

        context.pose.current_x = transformed_point.x
        context.pose.current_y = transformed_point.y
        context.pose.current_z = target_z

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=instruction.line_number,
            raw_text=(
                f'# MOVE_PALLET: {name}[{index}] -> '
                f'X={transformed_point.x:.2f} Y={transformed_point.y:.2f} '
                f'Z={target_z:.2f}'
            ),
            parameters={
                InstructionParam.X: transformed_point.x,
                InstructionParam.Y: transformed_point.y,
                InstructionParam.Z: target_z,
                InstructionParam.PHI: context.pose.current_phi,
                InstructionParam.SPEED: context.speed.current_speed,
            },
        )

        return (move_inst,)
