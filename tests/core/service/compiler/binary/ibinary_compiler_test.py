# -*- coding: UTF-8 -*-

'''
Module
    ibinary_compiler_test.py
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
    Unit tests for IBinaryCompiler protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyBinaryCompiler:
    '''Dummy binary compiler for protocol runtime check verification.'''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''Dummy compile_plan implementation.'''
        _ = plan
        return BinaryProgram(
            steps=(),
            raw_bytes=b'',
            total_duration_us=0,
            instruction_count=0,
            step_counts=(0, 0, 0, 0),
            telemetry=BinaryProgramTelemetry(),
        )

    def get_version(self) -> str:
        '''Dummy get_version implementation.'''
        return '1.0.0'


class TestIBinaryCompiler(TestCase):
    '''
        Test cases verifying IBinaryCompiler protocol contract.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies dummy class satisfies protocol.
                | test_negative_protocol_conformance - Verifies non-conforming class fails protocol.
    '''

    def test_protocol_conformance(self) -> None:
        '''Verifies structural typing conformance without inheritance.'''
        compiler = DummyBinaryCompiler()
        self.assertIsInstance(compiler, IBinaryCompiler)

    def test_negative_protocol_conformance(self) -> None:
        '''Verifies object() fails IBinaryCompiler protocol.'''
        self.assertFalse(isinstance(object(), IBinaryCompiler))



if __name__ == '__main__':
    main()
