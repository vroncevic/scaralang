# -*- coding: UTF-8 -*-

'''
Module
    expander.py
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
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.model.dsl.macro.pallet import PalletDefinition
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.pose.point_3d import Point3D
from scaralang.core.service.compiler.macro.pallet.dependencies import PalletDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PalletMacroExpander:
    '''
        Macro expander managing pallet matrix layout definitions and calculating cell index targets.

        It defines:

            :attributes:
                | _dependencies - Parameter bundle with injected frame transformer.
            :methods:
                | __init__ - Initializes pallet macro expander with dependencies bundle.
                | can_expand - Checks if instruction is PALLET_DEF or MOVE_PALLET.
                | expand - Registers pallet or translates MOVE_PALLET into Cartesian motion.
    '''

    _dependencies: PalletDependencies

    def __init__(
        self,
        *,
        dependencies: PalletDependencies,
    ) -> None:
        '''
            Initializes PalletMacroExpander with injected dependencies bundle.

            :param dependencies: Injected PalletDependencies instance.
            :exceptions: None.
        '''
        self._dependencies: Final[PalletDependencies] = dependencies

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
        context: CompilerContext,
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
        name: str = str(params.get(ScaraInstructionParam.NAME, 'DEFAULT')).upper()

        if instruction.command_type == ScaraCommandType.PALLET_DEF:
            rows = int(params.get(ScaraInstructionParam.ROWS, 1))
            cols = int(params.get(ScaraInstructionParam.COLS, 1))

            if rows <= 0 or cols <= 0:
                raise ScaraSemanticError(
                    f'Error at line {instruction.line_number}: '
                    f'Pallet {name!r} rows and cols must be greater than zero, '
                    f'got rows={rows}, cols={cols}'
                )

            context.pallets[name] = PalletDefinition(
                name=name,
                rows=rows,
                cols=cols,
                dx=float(params.get(ScaraInstructionParam.DX, 20.0)),
                dy=float(params.get(ScaraInstructionParam.DY, 20.0)),
                start=Point2D(
                    x=float(params.get(ScaraInstructionParam.START_X, context.pose.current_x)),
                    y=float(params.get(ScaraInstructionParam.START_Y, context.pose.current_y)),
                ),
            )

            return ()

        if name not in context.pallets:
            raise ScaraSemanticError(
                f'Error at line {instruction.line_number}: '
                f'Pallet {name!r} is not defined before MOVE_PALLET'
            )

        pallet = context.pallets[name]
        index = int(params.get(ScaraInstructionParam.INDEX, 0))
        max_cells: int = pallet.rows * pallet.cols

        if index < 0 or index >= max_cells:
            raise ScaraSemanticError(
                f'Error at line {instruction.line_number}: '
                f'Pallet index {index} out of bounds for pallet {name!r} '
                f'(capacity: {max_cells} cells, valid range: 0..{max_cells - 1})'
            )

        pt: Point3D = self._dependencies.frame_transformer.transform_point(
            frame=context.active_frame,
            point=Point3D(
                x=pallet.start.x + (index % pallet.cols) * pallet.dx,
                y=pallet.start.y + (index // pallet.cols) * pallet.dy,
                z=(
                    float(params[ScaraInstructionParam.Z])
                    if ScaraInstructionParam.Z in params
                    else context.pose.current_z - context.active_frame.origin.z
                ),
            ),
        )

        context.pose.current_x = pt.x
        context.pose.current_y = pt.y
        context.pose.current_z = pt.z

        return (
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_L,
                line_number=instruction.line_number,
                raw_text=(
                    f'# MOVE_PALLET: {name}[{index}] -> '
                    f'X={pt.x:.2f} Y={pt.y:.2f} Z={pt.z:.2f}'
                ),
                parameters={
                    ScaraInstructionParam.X: pt.x,
                    ScaraInstructionParam.Y: pt.y,
                    ScaraInstructionParam.Z: pt.z,
                    ScaraInstructionParam.PHI: context.pose.current_phi,
                    ScaraInstructionParam.SPEED: context.speed.current_speed,
                },
            ),
        )
