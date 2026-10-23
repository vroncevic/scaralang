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
    Unit tests for SubroutineExpander component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.compiler.macro.segmenter.segmenter import BlockSegmenter
from scaralang.core.service.compiler.macro.subroutine.expander import SubroutineExpander
from scaralang.core.service.compiler.macro.subroutine.iexpander import ISubroutineExpander
from scaralang.core.service.compiler.macro.subroutine.registry import SubroutineRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineExpanderTest(TestCase):
    '''Test cases verifying SubroutineExpander inlining and error logic.'''

    def test_protocol_and_version(self) -> None:
        '''
            Verifies structural protocol adherence and version reporting.

            :exceptions: None.
        '''
        expander = SubroutineExpander(
            registry=SubroutineRegistry(),
            segmenter=BlockSegmenter(),
        )
        self.assertIsInstance(expander, ISubroutineExpander)
        self.assertEqual(expander.get_version(), '1.1.0')

    def test_expand_subroutine_def_and_call(self) -> None:
        '''
            Verifies that DEF registers subroutine and CALL inlines its body.

            :exceptions: None.
        '''
        expander = SubroutineExpander(
            registry=SubroutineRegistry(),
            segmenter=BlockSegmenter(),
        )
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.DEF,
                line_number=1,
                raw_text='DEF PICK',
                parameters={ScaraInstructionParam.NAME: 'PICK'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                line_number=2,
                raw_text='HOME',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=3,
                raw_text='END',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CALL,
                line_number=4,
                raw_text='CALL PICK',
                parameters={ScaraInstructionParam.NAME: 'PICK'},
            ),
        )

        expanded = expander.expand_subroutines(instructions=instructions)
        self.assertEqual(len(expanded), 1)
        self.assertEqual(expanded[0].command_type, ScaraCommandType.HOME)

    def test_subroutine_with_repeat_preserves_structure(self) -> None:
        '''
            Verifies that REPEAT block structure is preserved while inlining calls inside.

            :exceptions: None.
        '''
        expander = SubroutineExpander(
            registry=SubroutineRegistry(),
            segmenter=BlockSegmenter(),
        )
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.DEF,
                line_number=1,
                raw_text='DEF STEP',
                parameters={ScaraInstructionParam.NAME: 'STEP'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_REL,
                line_number=2,
                raw_text='MOVE_REL X:5.0',
                parameters={ScaraInstructionParam.X: 5.0},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=3,
                raw_text='END',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.REPEAT,
                line_number=4,
                raw_text='REPEAT 2',
                parameters={ScaraInstructionParam.COUNT: 2},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CALL,
                line_number=5,
                raw_text='CALL STEP',
                parameters={ScaraInstructionParam.NAME: 'STEP'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=6,
                raw_text='END',
                parameters={},
            ),
        )

        expanded = expander.expand_subroutines(instructions=instructions)
        self.assertEqual(len(expanded), 3)
        self.assertEqual(expanded[0].command_type, ScaraCommandType.REPEAT)
        self.assertEqual(expanded[1].command_type, ScaraCommandType.MOVE_REL)
        self.assertEqual(expanded[2].command_type, ScaraCommandType.END)

    def test_orphaned_end_raises(self) -> None:
        '''
            Verifies that isolated END statement raises ScaraSyntaxError.

            :exceptions: None.
        '''
        expander = SubroutineExpander(
            registry=SubroutineRegistry(),
            segmenter=BlockSegmenter(),
        )
        inst_end = ScaraInstruction(
            command_type=ScaraCommandType.END,
            line_number=1,
            raw_text='END',
            parameters={},
        )
        with self.assertRaises(ScaraSyntaxError):
            expander.expand_subroutines(instructions=(inst_end,))

    def test_recursion_limit_raises(self) -> None:
        '''
            Verifies that recursive subroutines trigger ScaraSemanticError on depth overflow.

            :exceptions: None.
        '''
        expander = SubroutineExpander(
            registry=SubroutineRegistry(),
            segmenter=BlockSegmenter(),
        )
        instructions = (
            ScaraInstruction(
                command_type=ScaraCommandType.DEF,
                line_number=1,
                raw_text='DEF RECURSE',
                parameters={ScaraInstructionParam.NAME: 'RECURSE'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CALL,
                line_number=2,
                raw_text='CALL RECURSE',
                parameters={ScaraInstructionParam.NAME: 'RECURSE'},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.END,
                line_number=3,
                raw_text='END',
                parameters={},
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.CALL,
                line_number=4,
                raw_text='CALL RECURSE',
                parameters={ScaraInstructionParam.NAME: 'RECURSE'},
            ),
        )

        with self.assertRaises(ScaraSemanticError):
            expander.expand_subroutines(instructions=instructions)


if __name__ == '__main__':
    main()
