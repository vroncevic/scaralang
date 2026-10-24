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
    Implementation of ZoneMacroExpander consuming declarative ZONE_DEF instructions.
'''

from __future__ import annotations

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.context import CompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ZoneMacroExpander:
    '''
        Macro expander processing and consuming declarative ZONE_DEF obstacle instructions.

        It defines:

            :methods:
                | __init__ - Initializes ZoneMacroExpander instance.
                | can_expand - Checks whether instruction is ZONE_DEF.
                | expand - Consumes ZONE_DEF instruction returning empty tuple.
                | get_version - Gets implementation version string.
    '''

    def __init__(self) -> None:
        '''Initializes ZoneMacroExpander instance.'''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks if instruction can be handled by zone macro expander.

            :param instruction: ScaraInstruction node to test.
            :return: True if ZONE_DEF, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type == ScaraCommandType.ZONE_DEF

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Processes and consumes declarative ZONE_DEF instruction.

            :param instruction: ScaraInstruction node to expand.
            :param context: Active mutable compiler context.
            :return: Empty tuple as ZONE_DEF generates no executable motion primitives.
            :exceptions: None.
        '''
        _ = instruction
        _ = context
        return ()

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
