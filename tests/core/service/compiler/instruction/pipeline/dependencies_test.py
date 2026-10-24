# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for PipelineDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.context import CompilerContext
from scaralang.core.model.trajectory.plan.waypoint import Waypoint
from scaralang.core.service.compiler.instruction.pipeline.dependencies import PipelineDependencies


class DummySubroutineExpander:
    '''Dummy subroutine expander for dependency tests.'''

    def expand_subroutines(
        self,
        *,
        instructions: tuple[ScaraInstruction, ...],
    ) -> tuple[ScaraInstruction, ...]:
        '''Dummy expand.'''
        _ = instructions
        return ()

    def get_version(self) -> str:
        '''Dummy version.'''
        return '1.1.1'


class DummyRepeatExpander:
    '''Dummy repeat expander for dependency tests.'''

    def expand_repeats(
        self,
        *,
        instructions: tuple[ScaraInstruction, ...],
    ) -> tuple[ScaraInstruction, ...]:
        '''Dummy expand.'''
        _ = instructions
        return ()

    def get_version(self) -> str:
        '''Dummy version.'''
        return '1.1.1'


class DummyProcessor:
    '''Dummy processor for dependency tests.'''

    def process_primitive(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''Dummy process.'''
        _ = (instruction, context)
        return ()

    def get_version(self) -> str:
        '''Dummy version.'''
        return '1.1.1'


class TestPipelineDependencies(TestCase):
    '''
        Test cases verifying PipelineDependencies parameter bundle.

        It defines:

            :methods:
                | test_initialization - Verifies initialization and properties.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies PipelineDependencies holds expanders and processor.

            :exceptions: None.
        '''
        subroutine_expander = DummySubroutineExpander()
        repeat_expander = DummyRepeatExpander()
        processor = DummyProcessor()
        deps = PipelineDependencies(
            subroutine_expander=subroutine_expander,
            repeat_expander=repeat_expander,
            macro_expanders=(),
            processor=processor,
        )
        self.assertIs(deps.subroutine_expander, subroutine_expander)
        self.assertIs(deps.repeat_expander, repeat_expander)
        self.assertEqual(deps.macro_expanders, ())
        self.assertIs(deps.processor, processor)


if __name__ == '__main__':
    main()
