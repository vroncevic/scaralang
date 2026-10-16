# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Coordinates compilation of Cartesian linear, joint, approach,
    retract, and arc motion DSL instructions.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.compiler_context import CompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.motion.isub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandCompiler:
    '''
        Sub-compiler coordinator handling motion instructions:
        MOVE_L, MOVE_J, APPROACH, RETRACT, ARC_CW, ARC_CCW.
        Delegates compilation directly to specialized sub-compilers
        conforming to IMotionSubCompiler.

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled ScaraCommandType instances.
                | _sub_compilers - Tuple of injected motion sub-compilers.
            :methods:
                | __init__ - Initializes motion compiler with injected sub-compilers.
                | can_compile - Checks if command is a motion instruction.
                | compile - Delegates compilation to matching sub-compiler.
                | get_version - Gets implementation version string.
    '''

    _SUPPORTED: frozenset[ScaraCommandType] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
        ScaraCommandType.APPROACH,
        ScaraCommandType.RETRACT,
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
    })

    _sub_compilers: tuple[IMotionSubCompiler, ...]

    def __init__(
        self,
        *,
        sub_compilers: tuple[IMotionSubCompiler, ...],
    ) -> None:
        '''
            Initializes MotionCommandCompiler with injected sub-compilers.

            :param sub_compilers: Injected tuple of motion sub-compilers.
            :exceptions: None.
        '''
        self._sub_compilers: Final[tuple[IMotionSubCompiler, ...]] = sub_compilers

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Determines whether this coordinator handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if handled, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type in self._SUPPORTED

    def compile(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Processes motion instructions by delegating to the appropriate sub-compiler.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :return: Tuple of compiled Waypoint instances.
            :exceptions: None.
        '''
        for sub_compiler in self._sub_compilers:
            if sub_compiler.can_compile(instruction=instruction):
                return sub_compiler.compile(
                    instruction=instruction,
                    context=context,
                )

        return ()

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
