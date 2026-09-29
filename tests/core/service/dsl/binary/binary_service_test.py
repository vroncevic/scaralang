# -*- coding: UTF-8 -*-

'''
Module
    binary_service_test.py
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
    Unit tests for BinaryService and BinaryServiceFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.dsl.binary.binary_service import BinaryService
from scaralang.core.service.dsl.binary.binary_service_factory import BinaryServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryService(TestCase):
    '''
        Test cases verifying BinaryService and BinaryServiceFactory.

        It defines:

            :methods:
                | test_compile_plan - Verifies delegation of compile_plan.
                | test_disassemble_bytes - Verifies delegation of disassemble.
                | test_get_program_telemetry - Verifies telemetry extraction.
                | test_factory - Verifies BinaryServiceFactory creation.
    '''

    def setUp(self) -> None:
        '''Sets up test mocks.'''
        self.mock_compiler = MagicMock()
        self.mock_disassembler = MagicMock()
        self.service = BinaryService(
            compiler=self.mock_compiler,
            disassembler=self.mock_disassembler,
        )

    def test_compile_plan(self) -> None:
        '''Verifies compile_plan delegates to compiler.'''
        mock_plan = MagicMock()
        telemetry = BinaryProgramTelemetry(
            source_instructions=0,
            compiled_steps=0,
            duration_us=0,
            duration_s=0.0,
            peak_j1_steps=0,
            peak_j2_steps=0,
            peak_z_steps=0,
            peak_j4_steps=0,
            total_wire_bytes=0,
        )
        mock_prog = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=telemetry,
        )
        self.mock_compiler.compile_plan.return_value = mock_prog

        result = self.service.compile_plan(plan=mock_plan)
        self.assertEqual(result, mock_prog)
        self.mock_compiler.compile_plan.assert_called_once_with(plan=mock_plan)

    def test_get_program_telemetry(self) -> None:
        '''Verifies get_program_telemetry extracts telemetry model.'''
        telemetry = BinaryProgramTelemetry(
            source_instructions=1,
            compiled_steps=2,
            duration_us=1000,
            duration_s=0.001,
            peak_j1_steps=10,
            peak_j2_steps=20,
            peak_z_steps=30,
            peak_j4_steps=40,
            total_wire_bytes=50,
        )
        program = BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(10, 20, 30, 40),
            telemetry=telemetry,
        )
        result = self.service.get_program_telemetry(program=program)
        self.assertEqual(result, telemetry)

    def test_disassemble_bytes(self) -> None:
        '''Verifies disassemble_bytes delegates to disassembler.'''
        frame = DisassembledFrame(
            index=0,
            seq_num=1,
            msg_id=1,
            msg_name='CMD_HOME',
            detail='Home calibration',
        )
        self.mock_disassembler.disassemble.return_value = (frame,)

        result = self.service.disassemble_bytes(data=b'\xaa\x55')
        self.assertEqual(result, (frame,))
        self.mock_disassembler.disassemble.assert_called_once_with(
            data=b'\xaa\x55'
        )

    def test_calculate_disassembly_summary(self) -> None:
        '''Verifies calculate_disassembly_summary delegates to disassembler.'''
        frame = DisassembledFrame(
            index=0,
            seq_num=1,
            msg_id=1,
            msg_name='CMD_HOME',
            detail='Home calibration',
        )
        expected_summary = DisassemblySummary(
            total_bytes=16,
            decoded_frames=1,
            motion_frames=0,
            tool_commands=0,
            wait_delays=0,
            system_frames=1,
        )
        self.mock_disassembler.calculate_summary.return_value = expected_summary

        result = self.service.calculate_disassembly_summary(
            frames=(frame,), byte_count=16
        )
        self.assertEqual(result, expected_summary)
        self.mock_disassembler.calculate_summary.assert_called_once_with(
            frames=(frame,), byte_count=16
        )

    def test_factory(self) -> None:
        '''Verifies factory creates wired service.'''
        service = BinaryServiceFactory.create(
            compiler=self.mock_compiler,
            disassembler=self.mock_disassembler,
        )
        self.assertIsInstance(service, BinaryService)
        self.assertEqual(BinaryServiceFactory.get_version(), '1.0.0')


if __name__ == '__main__':
    main()
