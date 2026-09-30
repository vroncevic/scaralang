# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_binary_compiler_test.py
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
    Unit tests for IScaraDslBinaryCompiler role interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.dsl.scara_dsl_bundle import ScaraDslBundle
from scaralang.core.service.dsl.scara_dsl_service import ScaraDslService
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockBinaryCompiler:
    '''
        Minimal mock class structurally implementing IScaraDslBinaryCompiler.
    '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles plan.
        '''
        _ = plan
        return MagicMock(spec=BinaryProgram)

    def compile_to_binary(self, *, source: str) -> BinaryProgram:
        '''
            Compiles source.
        '''
        _ = source
        return MagicMock(spec=BinaryProgram)

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles to bytes.
        '''
        _ = source
        return b''

    def get_program_telemetry(
        self, *, program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Gets telemetry.
        '''
        _ = program
        return MagicMock(spec=BinaryProgramTelemetry)


class TestIScaraDslBinaryCompiler(TestCase):
    '''
        Test cases verifying IScaraDslBinaryCompiler interface contract.

        It defines:

            :methods:
                | test_structural_typing_scara_dsl_service - Verifies ScaraDslService satisfies protocol.
                | test_structural_typing_mock - Verifies mock implementation satisfies protocol.
                | test_incompatible_type - Verifies incompatible object does not satisfy protocol.
    '''

    def test_structural_typing_scara_dsl_service(self) -> None:
        '''
            Verifies ScaraDslService structurally implements IScaraDslBinaryCompiler.
        '''
        bundle = ScaraDslBundle(
            compiler=MagicMock(),
            validator=MagicMock(),
            exporter=MagicMock(),
            binary_service=MagicMock(),
            toolchain_info=MagicMock(),
        )
        service = ScaraDslService(bundle=bundle)
        self.assertIsInstance(service, IScaraDslBinaryCompiler)

    def test_structural_typing_mock(self) -> None:
        '''
            Verifies custom mock implementation satisfies IScaraDslBinaryCompiler.
        '''
        mock_compiler = MockBinaryCompiler()
        self.assertIsInstance(mock_compiler, IScaraDslBinaryCompiler)

    def test_incompatible_type(self) -> None:
        '''
            Verifies object missing protocol methods fails isinstance check.
        '''
        self.assertNotIsInstance(object(), IScaraDslBinaryCompiler)


if __name__ == '__main__':
    main()
