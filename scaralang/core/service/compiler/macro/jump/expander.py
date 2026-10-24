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
    Implementation of IMacroExpander expanding high-speed JUMP arch pick-and-place trajectories.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.compiler.context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JumpMacroExpander:
    '''
        Macro expander generating 3D parabolic clearance trajectories for JUMP commands.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction is of type JUMP.
                | expand - Expands JUMP instruction into vertical lift, transit, and descent.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks whether this expander handles JUMP instructions.

            :param instruction: ScaraInstruction node to check.
            :return: True if instruction is JUMP, False otherwise.
        '''
        return instruction.command_type == ScaraCommandType.JUMP

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Expands JUMP into 3-phase 3D clearance motion.

            :param instruction: JUMP instruction node.
            :param context: Active compiler context.
            :return: Tuple of expanded motion instructions.
        '''
        params = instruction.parameters
        target_x: float = float(
            params.get(ScaraInstructionParam.X, context.pose.current_x)
        )
        target_y: float = float(
            params.get(ScaraInstructionParam.Y, context.pose.current_y)
        )
        target_z: float = float(params.get(ScaraInstructionParam.Z, 0.0))
        target_phi: float = float(
            params.get(ScaraInstructionParam.PHI, context.pose.current_phi)
        )
        arch_height: float = float(
            params.get(ScaraInstructionParam.ARCH_HEIGHT, 20.0)
        )
        speed: float = float(
            params.get(ScaraInstructionParam.SPEED, context.speed.speed_rapid)
        )

        clearance_z = max(context.pose.current_z, target_z) + arch_height
        line_num = instruction.line_number

        lift_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=line_num,
            raw_text=f'# JUMP phase 1 (Lift): Z={clearance_z:.2f}',
            parameters={
                ScaraInstructionParam.X: context.pose.current_x,
                ScaraInstructionParam.Y: context.pose.current_y,
                ScaraInstructionParam.Z: clearance_z,
                ScaraInstructionParam.PHI: context.pose.current_phi,
                ScaraInstructionParam.SPEED: speed,
            },
        )

        transit_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_J,
            line_number=line_num,
            raw_text=f'# JUMP phase 2 (Transit): X={target_x:.2f} Y={target_y:.2f}',
            parameters={
                ScaraInstructionParam.X: target_x,
                ScaraInstructionParam.Y: target_y,
                ScaraInstructionParam.Z: clearance_z,
                ScaraInstructionParam.PHI: target_phi,
                ScaraInstructionParam.SPEED: speed,
            },
        )

        descend_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=line_num,
            raw_text=f'# JUMP phase 3 (Descent): Z={target_z:.2f}',
            parameters={
                ScaraInstructionParam.X: target_x,
                ScaraInstructionParam.Y: target_y,
                ScaraInstructionParam.Z: target_z,
                ScaraInstructionParam.PHI: target_phi,
                ScaraInstructionParam.SPEED: speed,
            },
        )

        context.pose.current_x = target_x
        context.pose.current_y = target_y
        context.pose.current_z = target_z
        context.pose.current_phi = target_phi

        return lift_inst, transit_inst, descend_inst
