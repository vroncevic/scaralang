# -*- coding: UTF-8 -*-

'''
Module
    primitive_instruction_processor.py
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
    Implementation of IPrimitiveInstructionProcessor dispatching primitive AST instructions.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Final

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PrimitiveInstructionProcessor:
    '''
        Processor dispatching primitive instructions across registered IPrimitiveCompiler instances.

        It defines:

            :attributes:
                | _primitive_compilers - Registered IPrimitiveCompiler components.
            :methods:
                | __init__ - Initializes processor with sequence of primitive sub-compilers.
                | process_primitive - Dispatches instruction to matching compiler.
                | get_version - Returns the processor version string.
    '''

    _primitive_compilers: tuple[IPrimitiveCompiler, ...]

    def __init__(
        self,
        *,
        primitive_compilers: Sequence[IPrimitiveCompiler],
    ) -> None:
        '''
            Initializes PrimitiveInstructionProcessor with injected compilers.

            :param primitive_compilers: Sequence of IPrimitiveCompiler components.
            :exceptions: None.
        '''
        self._primitive_compilers: Final[tuple[IPrimitiveCompiler, ...]] = tuple(primitive_compilers)

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
        for compiler in self._primitive_compilers:
            if compiler.can_compile(instruction=instruction):
                return compiler.compile(
                    instruction=instruction,
                    context=context,
                )

        raise ValueError(
            f'Unsupported or unhandled instruction: {instruction.command_type}'
        )

    def get_version(self) -> str:
        '''
            Returns the processor version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
