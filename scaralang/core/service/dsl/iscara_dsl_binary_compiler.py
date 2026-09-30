# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_binary_compiler.py
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
    Defines role interface IScaraDslBinaryCompiler for binary wire compilation and telemetry.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslBinaryCompiler(Protocol):
    '''
        Role interface protocol for SCARA DSL binary wire compilation and telemetry.

        It defines:

            :methods:
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | compile_to_binary - Compiles DSL source text into BinaryProgram package.
                | compile_to_bytes - Compiles DSL code directly to raw UART wire byte stream.
                | get_program_telemetry - Returns execution metrics and telemetry
                  for binary program.
    '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles ITrajectoryPlan into BinaryProgram package.

            :param plan: ITrajectoryPlan protocol instance.
            :return: Compiled BinaryProgram package.
            :exceptions: None.
        '''

    def compile_to_binary(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source text into BinaryProgram package.

            :param source: Raw .scara DSL source text.
            :return: Compiled BinaryProgram package.
            :exceptions: None.
        '''

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL code directly to raw UART wire byte stream.

            :param source: Raw .scara DSL source text.
            :return: Serialized wire byte stream.
            :exceptions: None.
        '''

    def get_program_telemetry(
        self, *, program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Returns execution metrics and telemetry for a compiled binary program.

            :param program: BinaryProgram instance.
            :return: BinaryProgramTelemetry domain model.
            :exceptions: None.
        '''
