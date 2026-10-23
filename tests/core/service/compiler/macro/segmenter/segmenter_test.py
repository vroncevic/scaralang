# -*- coding: UTF-8 -*-

'''
Module
    segmenter_test.py
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
    Unit tests for BlockSegmenter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.compiler.macro.segmenter.isegmenter import ISegmenter
from scaralang.core.service.compiler.macro.segmenter.segmenter import BlockSegmenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BlockSegmenterTest(TestCase):
    '''Test cases verifying BlockSegmenter block isolation and error handling.'''

    def test_protocol_and_version(self) -> None:
        '''
            Verifies protocol implementation and version reporting.

            :exceptions: None.
        '''
        segmenter = BlockSegmenter()
        self.assertIsInstance(segmenter, ISegmenter)
        self.assertEqual(segmenter.get_version(), '1.1.0')

    def test_single_block_segmentation(self) -> None:
        '''
            Verifies segmenting a single non-nested block.

            :exceptions: None.
        '''
        segmenter = BlockSegmenter()
        inst_def = ScaraInstruction(
            command_type=ScaraCommandType.DEF,
            line_number=1,
            raw_text='DEF ROUTINE',
            parameters={ScaraInstructionParam.NAME: 'ROUTINE'},
        )
        inst_home = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            line_number=2,
            raw_text='HOME',
            parameters={},
        )
        inst_end = ScaraInstruction(
            command_type=ScaraCommandType.END,
            line_number=3,
            raw_text='END',
            parameters={},
        )
        instructions = (inst_def, inst_home, inst_end)

        end_idx, body = segmenter.segment_block(
            instructions=instructions, start_index=0
        )
        self.assertEqual(end_idx, 2)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0].command_type, ScaraCommandType.HOME)

    def test_nested_block_segmentation(self) -> None:
        '''
            Verifies that nested blocks are tracked properly by depth.

            :exceptions: None.
        '''
        segmenter = BlockSegmenter()
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.DEF,
                line_number=10,
                raw_text='DEF nested_pick',
                parameters={ScaraInstructionParam.NAME: 'nested_pick'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.REPEAT,
                line_number=11,
                raw_text='REPEAT 4',
                parameters={ScaraInstructionParam.COUNT: 4},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.WAIT_MS,
                line_number=12,
                raw_text='WAIT_MS 250',
                parameters={ScaraInstructionParam.MS: 250},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=13,
                raw_text='END',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=14,
                raw_text='END',
                parameters={},
            ),
        )

        end_idx, body = segmenter.segment_block(
            instructions=instructions, start_index=0
        )
        self.assertEqual(end_idx, 4)
        self.assertEqual(len(body), 3)

    def test_unterminated_block_raises(self) -> None:
        '''
            Verifies that missing matching END raises ScaraSyntaxError.

            :exceptions: None.
        '''
        segmenter = BlockSegmenter()
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.DEF,
                line_number=1,
                raw_text='DEF BROKEN',
                parameters={ScaraInstructionParam.NAME: 'BROKEN'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                line_number=2,
                raw_text='HOME',
                parameters={},
            ),
        )

        with self.assertRaises(ScaraSyntaxError):
            segmenter.segment_block(instructions=instructions, start_index=0)


if __name__ == '__main__':
    main()
