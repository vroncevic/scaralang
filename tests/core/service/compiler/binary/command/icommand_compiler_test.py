# -*- coding: UTF-8 -*-

'''
Module
    icommand_compiler_test.py
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
    Unit tests for ICommandCompiler protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyCommandCompiler:
    '''
        Dummy class implementing ICommandCompiler for protocol verification.
    '''

    def compile_command_step(
        self,
        *,
        command: str,
        seq_num: int,
        line_num: int,
    ) -> Step:
        '''
            Dummy implementation of compile_command_step.
        '''
        frame = BinaryFrame(
            seq_num=seq_num,
            msg_id=MessageId.CMD_HOME,
            payload=b'',
            crc16=0,
        )
        return Step(
            frame=frame,
            raw_bytes=b'',
            duration_us=1000,
            target_steps=(0, 0, 0, 0),
            description=command,
            line_number=line_num,
        )


class TestICommandCompiler(TestCase):
    '''
        Test cases verifying ICommandCompiler structural protocol.

        It defines:

            :methods:
                | test_structural_conformance - Verifies protocol check.
                | test_structural_rejection - Verifies incomplete dummy is rejected.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies that dummy conforming class satisfies protocol check.
        '''
        compiler = DummyCommandCompiler()
        self.assertIsInstance(compiler, ICommandCompiler)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that class missing required methods fails protocol check.
        '''
        class IncompleteCompiler:
            '''Dummy incomplete compiler for negative test.'''

        self.assertNotIsInstance(IncompleteCompiler(), ICommandCompiler)


if __name__ == '__main__':
    main()
