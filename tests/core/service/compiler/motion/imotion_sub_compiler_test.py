# -*- coding: UTF-8 -*-

'''
Module
    imotion_sub_compiler_test.py
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
    Unit tests for IMotionSubCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyMotionSubCompiler:
    '''
        Dummy class implementing IMotionSubCompiler for runtime checkable verification.
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
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Dummy implementation of compile.
        '''
        _ = instruction
        _ = context
        _ = waypoints


class IncompleteMotionSubCompiler:
    '''
        Incomplete dummy class missing compile method.
    '''

    def can_compile(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Dummy implementation of can_compile.
        '''
        _ = instruction
        return False


class TestIMotionSubCompiler(TestCase):
    '''
        Test cases verifying IMotionSubCompiler protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        compiler = DummyMotionSubCompiler()
        self.assertIsInstance(compiler, IMotionSubCompiler)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        compiler = IncompleteMotionSubCompiler()
        self.assertNotIsInstance(compiler, IMotionSubCompiler)


if __name__ == '__main__':
    main()
