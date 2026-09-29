# -*- coding: UTF-8 -*-

'''
Module
    frame_macro_expander.py
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
    Implementation of IMacroExpander tracking and transforming coordinates according to work frames.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import InstructionParam
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.dsl.macro.work_frame import WorkFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameMacroExpander:
    '''
        Macro expander managing local work coordinate frames and transforming Cartesian points.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if instruction is FRAME_SET or FRAME_RESET.
                | expand - Updates active frame in compiler context and emits marker comment.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks whether this expander handles frame setup commands.

            :param instruction: ScaraInstruction node to check.
            :return: True if FRAME_SET or FRAME_RESET, False otherwise.
        '''
        return instruction.command_type in (
            ScaraCommandType.FRAME_SET,
            ScaraCommandType.FRAME_RESET,
        )

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Updates compiler context frame transformation parameters.

            :param instruction: Frame instruction node.
            :param context: Active compiler context.
            :return: Tuple containing empty or informational comment instruction.
        '''
        if instruction.command_type == ScaraCommandType.FRAME_RESET:
            context.active_frame = WorkFrame(x=0.0, y=0.0, angle_deg=0.0)
        else:
            params = instruction.parameters
            raw_angle = params.get(
                InstructionParam.ANGLE, params.get(InstructionParam.RZ, 0.0)
            )
            context.active_frame = WorkFrame(
                x=float(params.get(InstructionParam.X, 0.0)),
                y=float(params.get(InstructionParam.Y, 0.0)),
                angle_deg=float(raw_angle),
            )

        return ()
