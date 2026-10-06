# -*- coding: UTF-8 -*-

'''
Module
    iprimitive_compiler_test.py
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
    Unit tests for IPrimitiveCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyPrimitiveCompiler:
    '''
        Dummy class implementing IPrimitiveCompiler for protocol verification.
    '''

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Dummy implementation of can_compile.
        '''
        _ = instruction
        return True

    def compile(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Dummy implementation of compile.
        '''
        _ = instruction
        _ = context
        return ()


class IncompletePrimitiveCompiler:  # pylint: disable=too-few-public-methods
    '''
        Incomplete dummy class missing compile method.
    '''

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Dummy implementation of can_compile.
        '''
        _ = instruction
        return False


class TestIPrimitiveCompiler(TestCase):
    '''
        Test cases verifying IPrimitiveCompiler protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        compiler = DummyPrimitiveCompiler()
        self.assertIsInstance(compiler, IPrimitiveCompiler)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        compiler = IncompletePrimitiveCompiler()
        self.assertNotIsInstance(compiler, IPrimitiveCompiler)


if __name__ == '__main__':
    main()
