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
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.compiler.instruction.pipeline.dependencies import PipelineDependencies


class DummyProcessor:
    '''Dummy processor for dependency tests.'''

    def process_primitive(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[Waypoint, ...]:
        '''Dummy process.'''
        _ = (instruction, context)
        return ()

    def get_version(self) -> str:
        '''Dummy version.'''
        return '1.0.8'


class TestPipelineDependencies(TestCase):
    '''
        Test cases verifying PipelineDependencies parameter bundle.

        It defines:

            :methods:
                | test_initialization - Verifies initialization and properties.
    '''

    def test_initialization(self) -> None:
        '''Verifies PipelineDependencies holds expanders and processor.'''
        processor = DummyProcessor()
        deps = PipelineDependencies(macro_expanders=(), processor=processor)
        self.assertEqual(deps.macro_expanders, ())
        self.assertIs(deps.processor, processor)


if __name__ == '__main__':
    main()
