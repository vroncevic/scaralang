# -*- coding: UTF-8 -*-

'''
Module
    instruction_test.py
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
    Unit tests for ScaraInstruction AST model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from operator import setitem
from types import MappingProxyType
from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraInstructionTest(TestCase):
    '''Unit tests validating ScaraInstruction AST node immutability and attributes.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper attribute initialization and mapping encapsulation.'''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            line_number=42,
            raw_text='MOVE_L X=100.0 Y=200.0 Z=10.0',
            parameters=MappingProxyType({'X': 100.0, 'Y': 200.0, 'Z': 10.0}),
        )
        self.assertEqual(instruction.command_type, ScaraCommandType.MOVE_L)
        self.assertEqual(instruction.line_number, 42)
        self.assertEqual(instruction.raw_text, 'MOVE_L X=100.0 Y=200.0 Z=10.0')
        self.assertEqual(instruction.parameters['X'], 100.0)
        self.assertEqual(instruction.parameters['Y'], 200.0)
        self.assertEqual(instruction.parameters['Z'], 10.0)
        self.assertIsInstance(instruction.parameters, MappingProxyType)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes raises FrozenInstanceError.'''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters=MappingProxyType({}),
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(instruction, 'line_number', 2)

    def test_parameters_mutation_rejected(self) -> None:
        '''Verify that mutating the parameters proxy raises TypeError.'''
        raw_dict = {'SPEED': 50.0}
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.SPEED,
            line_number=5,
            raw_text='SPEED 50',
            parameters=MappingProxyType(raw_dict),
        )
        with self.assertRaises(TypeError):
            setitem(instruction.parameters, 'SPEED', 100.0)


if __name__ == '__main__':
    main()
