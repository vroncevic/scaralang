# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_test.py
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
    Unit tests for ScaraCompiler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.dsl.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.scara_compiler import ScaraCompiler
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraCompiler(TestCase):
    '''
        Test cases verifying ScaraCompiler compilation and validation.

        It defines:

            :methods:
                | setUp - Initializes test compiler with mock collaborators.
                | test_structural_conformance - Verifies protocol check.
                | test_compile - Verifies primary compile method.
                | test_compile_bytes - Verifies compile_bytes method.
                | test_compile_plan - Verifies plan compilation delegation.
                | test_compile_to_binary - Verifies compile_to_binary method.
                | test_compile_to_bytes - Verifies compile_to_bytes method.
                | test_get_program_telemetry - Verifies telemetry extraction.
                | test_get_version - Verifies version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up compiler with mocked collaborators.
        '''
        self.mock_dsl_compiler = MagicMock(spec=IScaraDslCompiler)
        self.mock_binary_compiler = MagicMock(spec=IBinaryCompiler)
        self.compiler = ScaraCompiler(
            compiler=self.mock_dsl_compiler,
            binary_compiler=self.mock_binary_compiler,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IScaraCompiler.
        '''
        self.assertIsInstance(self.compiler, IScaraCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies compiler get_version returns semantic version string.
        '''
        self.assertEqual(self.compiler.get_version(), '1.0.4')

    def test_compile(self) -> None:
        '''
            Verifies compile delegates to compile_to_binary.
        '''
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        self.mock_dsl_compiler.compile_script.return_value = mock_plan
        self.mock_binary_compiler.compile_plan.return_value = mock_program

        result = self.compiler.compile(source='HOME\n')
        self.assertEqual(result, mock_program)
        self.mock_dsl_compiler.compile_script.assert_called_once_with(source='HOME\n')
        self.mock_binary_compiler.compile_plan.assert_called_once_with(plan=mock_plan)

    def test_compile_bytes(self) -> None:
        '''
            Verifies compile_bytes returns raw bytes from compiled program.
        '''
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.raw_bytes = b'\x01\x02\x03'
        self.mock_dsl_compiler.compile_script.return_value = mock_plan
        self.mock_binary_compiler.compile_plan.return_value = mock_program

        result = self.compiler.compile_bytes(source='HOME\n')
        self.assertEqual(result, b'\x01\x02\x03')

    def test_compile_plan(self) -> None:
        '''
            Verifies compile_plan delegates directly to binary compiler.
        '''
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        self.mock_binary_compiler.compile_plan.return_value = mock_program

        result = self.compiler.compile_plan(plan=mock_plan)
        self.assertEqual(result, mock_program)
        self.mock_binary_compiler.compile_plan.assert_called_once_with(plan=mock_plan)

    def test_compile_to_binary(self) -> None:
        '''
            Verifies compile_to_binary compiles script to plan and plan to binary.
        '''
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        self.mock_dsl_compiler.compile_script.return_value = mock_plan
        self.mock_binary_compiler.compile_plan.return_value = mock_program

        result = self.compiler.compile_to_binary(source='MOVE_J X=10\n')
        self.assertEqual(result, mock_program)

    def test_compile_to_bytes(self) -> None:
        '''
            Verifies compile_to_bytes extracts raw bytes.
        '''
        mock_plan = MagicMock(spec=ITrajectoryPlan)
        mock_program = MagicMock(spec=BinaryProgram)
        mock_program.raw_bytes = b'\xaa\xbb'
        self.mock_dsl_compiler.compile_script.return_value = mock_plan
        self.mock_binary_compiler.compile_plan.return_value = mock_program

        result = self.compiler.compile_to_bytes(source='MOVE_J X=10\n')
        self.assertEqual(result, b'\xaa\xbb')

    def test_get_program_telemetry(self) -> None:
        '''
            Verifies get_program_telemetry extracts telemetry from program.
        '''
        mock_program = MagicMock(spec=BinaryProgram)
        mock_telemetry = MagicMock(spec=BinaryProgramTelemetry)
        mock_program.telemetry = mock_telemetry

        result = self.compiler.get_program_telemetry(program=mock_program)
        self.assertEqual(result, mock_telemetry)


if __name__ == '__main__':
    main()
