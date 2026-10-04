# -*- coding: UTF-8 -*-

'''
Module
    iprimitive_instruction_processor.py
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
    Defines structural protocol IPrimitiveInstructionProcessor for
    processing primitive instructions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPrimitiveInstructionProcessor(Protocol):
    '''
        Structural protocol defining contracts for processing primitive instructions.

        It defines:

            :methods:
                | process_primitive - Dispatches primitive instruction to matching sub-compiler.
                | get_version - Returns the processor version string.
    '''

    def process_primitive(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Dispatches primitive AST instruction to matching primitive sub-compiler.

            :param instruction: ScaraInstruction node to process.
            :param context: Active mutable compiler context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: ValueError if instruction is not handled by any compiler.
        '''

    def get_version(self) -> str:
        '''
            Returns the processor version string representation.

            :return: Version string representation.
        '''
