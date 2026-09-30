# -*- coding: UTF-8 -*-

'''
Module
    disassemble_command_executor_test.py
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
    Unit tests for DisassembleCommandExecutor class.
'''

from __future__ import annotations

from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main

from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.infrastructure.command.compile.compile_command_executor_factory import CompileCommandExecutorFactory
from scaralang.infrastructure.command.disassemble.disassemble_command_definition import DisassembleCommandDefinition
from scaralang.infrastructure.command.disassemble.disassemble_command_executor import DisassembleCommandExecutor
from scaralang.infrastructure.command.disassemble.format.disassemble_summary_formatter_factory import DisassembleSummaryFormatterFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker_factory import BinaryPayloadUnpackerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisassembleCommandExecutor(TestCase):
    '''
        Test cases verifying DisassembleCommandExecutor.

        It defines:

            :methods:
                | setUp - Initializes fixtures.
                | tearDown - Cleans up temporary resources.
                | test_disassemble_missing_file - Verifies handling of absent file.
                | test_disassemble_compiled_file - Verifies disassembling valid binary file.
                | test_disassemble_summary - Verifies disassemble with summary option.
                | test_get_definition - Verifies definition retrieval.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.
        '''
        self.cmd_def = DisassembleCommandDefinition()
        self.summary_formatter = DisassembleSummaryFormatterFactory.create()
        self.executor = DisassembleCommandExecutor(
            definition=self.cmd_def,
            summary_formatter=self.summary_formatter,
        )
        self.service = ScaraDslServiceFactory.create_default(
            frame_builder=BinaryFrameBuilderFactory.create(),
            frame_parser=BinaryFrameParserFactory.create_default(),
            payload_unpacker=BinaryPayloadUnpackerFactory.create(),
        )
        self.temp_files: list[str] = []

    def tearDown(self) -> None:
        '''
            Cleans up temporary resources.
        '''
        for path in self.temp_files:
            if exists(path):
                remove(path)

    def create_source_file(self, content: str) -> str:
        '''
            Creates temporary source file helper.
        '''
        with NamedTemporaryFile(mode='w', suffix='.scara', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_name = f.name
        self.temp_files.append(temp_name)
        return temp_name

    def test_disassemble_missing_file(self) -> None:
        '''
            Verifies handling of non-existent input binary file.
        '''
        res = self.executor.execute(
            params={'file': '/nonexistent/file.bin'},
            service=self.service,
        )
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('does not exist', str(res.get('stderr', '')))

    def test_disassemble_compiled_file(self) -> None:
        '''
            Verifies end-to-end compile to binary file and disassembly.
        '''
        script_path = self.create_source_file('HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n')
        bin_path = script_path + '.bin'
        self.temp_files.append(bin_path)

        compile_exec = CompileCommandExecutorFactory.create_default()
        compile_exec.execute(
            params={'script': script_path, 'output': bin_path},
            service=self.service,
        )

        res = self.executor.execute(params={'file': bin_path}, service=self.service)
        self.assertEqual(res.get('returncode'), 0)
        disasm_out = str(res.get('stdout', ''))
        self.assertIn('CMD_HOME', disasm_out)
        self.assertIn('CMD_MOVE_JOINT_STEPS', disasm_out)
        self.assertIn('PUMP ON', disasm_out)

    def test_disassemble_summary(self) -> None:
        '''
            Verifies disassemble command with stream summary enabled.
        '''
        script_path = self.create_source_file('HOME\nPUMP ON\n')
        bin_path = script_path + '.bin'
        self.temp_files.append(bin_path)

        compile_exec = CompileCommandExecutorFactory.create_default()
        compile_exec.execute(
            params={'script': script_path, 'output': bin_path},
            service=self.service,
        )

        res = self.executor.execute(
            params={'file': bin_path, 'summary': True},
            service=self.service,
        )
        self.assertEqual(res.get('returncode'), 0)
        stdout_text = str(res.get('stdout', ''))
        self.assertIn('Disassembly Summary:', stdout_text)
        self.assertIn('Total Decoded Frames: 2', stdout_text)
        self.assertIn('Tool Commands:', stdout_text)

    def test_get_definition(self) -> None:
        '''
            Verifies definition getter.
        '''
        self.assertEqual(self.executor.get_definition(), self.cmd_def)


if __name__ == '__main__':
    main()
