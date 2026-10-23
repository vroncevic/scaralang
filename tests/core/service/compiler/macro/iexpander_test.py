# -*- coding: UTF-8 -*-

'''
Module
    iexpander_test.py
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
    Unit tests for IMacroExpander protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyExpander:
    '''
        Dummy class implementing IMacroExpander structurally.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks handling of instruction.
        '''
        _ = instruction
        return True

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Expands instruction.
        '''
        _ = instruction
        _ = context
        return ()


class NonExpander:
    '''
        Incomplete class missing expand method.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks handling.
        '''
        _ = instruction
        return False

    def dummy(self) -> None:
        '''
            Dummy method for method count.
        '''



class TestIMacroExpander(TestCase):
    '''
        Test cases for IMacroExpander runtime checkability.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol check for valid and invalid classes.
        '''
        dummy = DummyExpander()
        self.assertIsInstance(dummy, IMacroExpander)

        invalid = NonExpander()
        self.assertNotIsInstance(invalid, IMacroExpander)


if __name__ == '__main__':
    main()
