# -*- coding: UTF-8 -*-

'''
Module
    repeat_test.py
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
    Unit testing for RepeatLoopDescriptor domain model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.macro.repeat import RepeatLoopDescriptor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RepeatTest(TestCase):
    '''
        Validates RepeatLoopDescriptor initialization, attributes, and immutability.
    '''

    def test_initialization_and_attributes(self) -> None:
        '''
            Verifies that valid parameters correctly populate fields.

            :exceptions: None.
        '''
        inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=5,
            raw_text='HOME',
            parameters={},
        )
        loop = RepeatLoopDescriptor(
            count=5,
            instructions=(inst,),
            line_number=4,
        )
        self.assertEqual(loop.count, 5)
        self.assertEqual(len(loop.instructions), 1)
        self.assertEqual(loop.line_number, 4)

    def test_immutability(self) -> None:
        '''
            Verifies that attempting mutation raises FrozenInstanceError.

            :exceptions: None.
        '''
        loop = RepeatLoopDescriptor(
            count=3,
            instructions=(),
            line_number=1,
        )
        with self.assertRaises(FrozenInstanceError):
            loop.count = 10  # type: ignore[misc]


if __name__ == '__main__':
    main()
