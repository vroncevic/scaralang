# -*- coding: UTF-8 -*-

'''
Module
    expander_test.py
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
    Unit tests for RepeatExpander component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.compiler.macro.repeat.expander import RepeatExpander
from scaralang.core.service.compiler.macro.repeat.iexpander import IRepeatExpander
from scaralang.core.service.compiler.macro.segmenter.segmenter import BlockSegmenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RepeatExpanderTest(TestCase):
    '''Test cases verifying RepeatExpander unrolling logic and error handling.'''

    def test_protocol_and_version(self) -> None:
        '''
            Verifies structural protocol adherence and version reporting.

            :exceptions: None.
        '''
        expander = RepeatExpander(segmenter=BlockSegmenter())
        self.assertIsInstance(expander, IRepeatExpander)
        self.assertEqual(expander.get_version(), '1.1.1')

    def test_expand_repeat_loop(self) -> None:
        '''
            Verifies that REPEAT unrolls body instructions N times.

            :exceptions: None.
        '''
        expander = RepeatExpander(segmenter=BlockSegmenter())
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.REPEAT,
                line_number=1,
                raw_text='REPEAT 3',
                parameters={ScaraInstructionParam.COUNT: 3},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_REL,
                line_number=2,
                raw_text='MOVE_REL X:10.0',
                parameters={ScaraInstructionParam.X: 10.0},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=3,
                raw_text='END',
                parameters={},
            ),
        )

        expanded = expander.expand_repeats(instructions=instructions)
        self.assertEqual(len(expanded), 3)
        for item in expanded:
            self.assertEqual(item.command_type, ScaraCommandType.MOVE_REL)

    def test_nested_repeat_loops(self) -> None:
        '''
            Verifies that nested REPEAT loops unroll correctly.

            :exceptions: None.
        '''
        expander = RepeatExpander(segmenter=BlockSegmenter())
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.REPEAT,
                line_number=1,
                raw_text='REPEAT 2',
                parameters={ScaraInstructionParam.COUNT: 2},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.REPEAT,
                line_number=2,
                raw_text='REPEAT 3',
                parameters={ScaraInstructionParam.COUNT: 3},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                line_number=3,
                raw_text='HOME',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=4,
                raw_text='END',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=5,
                raw_text='END',
                parameters={},
            ),
        )

        expanded = expander.expand_repeats(instructions=instructions)
        self.assertEqual(len(expanded), 6)
        for item in expanded:
            self.assertEqual(item.command_type, ScaraCommandType.HOME)

    def test_orphaned_end_raises(self) -> None:
        '''
            Verifies that isolated END statement raises ScaraSyntaxError.

            :exceptions: None.
        '''
        expander = RepeatExpander(segmenter=BlockSegmenter())
        inst_end = ScaraInstruction(
            command_type=ScaraCommandType.END,
            line_number=1,
            raw_text='END',
            parameters={},
        )
        with self.assertRaises(ScaraSyntaxError):
            expander.expand_repeats(instructions=(inst_end,))


if __name__ == '__main__':
    main()
