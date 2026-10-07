# -*- coding: UTF-8 -*-

'''
Module
    iprimitive_instruction_processor_test.py
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
    Unit tests for IPrimitiveInstructionProcessor protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.iprimitive_instruction_processor import IPrimitiveInstructionProcessor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyPrimitiveInstructionProcessor:
    '''
        Dummy class implementing IPrimitiveInstructionProcessor for protocol verification.
    '''

    def process_primitive(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''
            Dummy implementation of process_primitive.
        '''
        _ = (instruction, context)
        return ()

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.7'


class TestIPrimitiveInstructionProcessor(TestCase):
    '''
        Test cases verifying IPrimitiveInstructionProcessor structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies that dummy conforming class satisfies protocol check.
        '''
        processor = DummyPrimitiveInstructionProcessor()
        self.assertIsInstance(processor, IPrimitiveInstructionProcessor)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that class missing required methods fails protocol check.
        '''
        self.assertFalse(isinstance(object(), IPrimitiveInstructionProcessor))


if __name__ == '__main__':
    main()
