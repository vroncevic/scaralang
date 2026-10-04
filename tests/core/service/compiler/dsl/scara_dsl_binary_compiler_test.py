# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_binary_compiler_test.py
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
    Unit tests for ScaraDslBinaryCompiler class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler import ScaraDslBinaryCompiler
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslBinaryCompiler(TestCase):
    '''
        Test cases verifying ScaraDslBinaryCompiler operations.

        It defines:

            :methods:
                | test_compile_plan - Verifies plan compilation delegation.
                | test_compile_to_binary - Verifies source compilation pipeline.
                | test_compile_to_bytes - Verifies raw bytes extraction.
                | test_get_program_telemetry - Verifies program telemetry retrieval.
                | test_structural_protocol_conformance - Verifies protocol satisfaction.
    '''

    def test_compile_plan(self) -> None:
        '''
            Verifies compile_plan delegates directly to binary compiler.
        '''
        mock_compiler = MagicMock()
        mock_binary_compiler = MagicMock()
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_binary_compiler.compile_plan.return_value = mock_program

        binary_compiler = ScaraDslBinaryCompiler(
            compiler=mock_compiler,
            binary_compiler=mock_binary_compiler,
        )
        result = binary_compiler.compile_plan(plan=mock_plan)
        self.assertEqual(result, mock_program)
        mock_binary_compiler.compile_plan.assert_called_once_with(plan=mock_plan)

    def test_compile_to_binary(self) -> None:
        '''
            Verifies compile_to_binary compiles source to plan then to binary program.
        '''
        mock_compiler = MagicMock()
        mock_binary_compiler = MagicMock()
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)

        mock_compiler.compile_script.return_value = mock_plan
        mock_binary_compiler.compile_plan.return_value = mock_program

        binary_compiler = ScaraDslBinaryCompiler(
            compiler=mock_compiler,
            binary_compiler=mock_binary_compiler,
        )
        result = binary_compiler.compile_to_binary(source='MOVE_L X=100 Y=100')
        self.assertEqual(result, mock_program)
        mock_compiler.compile_script.assert_called_once_with(source='MOVE_L X=100 Y=100')
        mock_binary_compiler.compile_plan.assert_called_once_with(plan=mock_plan)

    def test_compile_to_bytes(self) -> None:
        '''
            Verifies compile_to_bytes returns raw bytes from compiled binary program.
        '''
        mock_compiler = MagicMock()
        mock_binary_compiler = MagicMock()
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.raw_bytes = b'\xAA\x55\x01\x00'

        mock_compiler.compile_script.return_value = mock_plan
        mock_binary_compiler.compile_plan.return_value = mock_program

        binary_compiler = ScaraDslBinaryCompiler(
            compiler=mock_compiler,
            binary_compiler=mock_binary_compiler,
        )
        raw = binary_compiler.compile_to_bytes(source='WAIT 500')
        self.assertEqual(raw, b'\xAA\x55\x01\x00')

    def test_get_program_telemetry(self) -> None:
        '''
            Verifies get_program_telemetry extracts telemetry model from binary program.
        '''
        mock_compiler = MagicMock()
        mock_binary_compiler = MagicMock()
        mock_telemetry = MagicMock(spec=BinaryProgramTelemetry)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.telemetry = mock_telemetry

        binary_compiler = ScaraDslBinaryCompiler(
            compiler=mock_compiler,
            binary_compiler=mock_binary_compiler,
        )
        telemetry = binary_compiler.get_program_telemetry(program=mock_program)
        self.assertEqual(telemetry, mock_telemetry)

    def test_structural_protocol_conformance(self) -> None:
        '''
            Verifies ScaraDslBinaryCompiler structurally satisfies IScaraDslBinaryCompiler.
        '''
        mock_compiler = MagicMock()
        mock_binary_compiler = MagicMock()

        binary_compiler = ScaraDslBinaryCompiler(
            compiler=mock_compiler,
            binary_compiler=mock_binary_compiler,
        )
        self.assertIsInstance(binary_compiler, IScaraDslBinaryCompiler)


if __name__ == '__main__':
    main()
