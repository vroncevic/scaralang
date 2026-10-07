# -*- coding: UTF-8 -*-

'''
Module
    iscara_compiler.py
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
    Defines structural runtime-checkable protocol IScaraCompiler for compiling
    SCARA DSL scripts directly into binary frame packages and byte streams.
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
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraCompiler(Protocol):
    '''
        Structural protocol defining end-to-end SCARA DSL compilation and telemetry.

        It defines:

            :methods:
                | compile - Compiles DSL source code into BinaryProgram package.
                | compile_bytes - Compiles DSL source code directly into wire byte stream.
                | compile_to_binary - Compiles DSL source code into BinaryProgram package.
                | compile_to_bytes - Compiles DSL source code into wire byte stream.
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | get_program_telemetry - Returns execution metrics and telemetry
                  for binary program.
                | get_version - Returns compiler version string.
    '''

    def compile(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source code into a binary program package.

            :param source: Raw .scara script text.
            :return: BinaryProgram package containing packed binary frames.
            :exceptions: ValueError if parsing or kinematic validation fails.
        '''

    def compile_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL source code directly into a binary wire byte stream.

            :param source: Raw .scara script text.
            :return: Raw byte stream suitable for UART transmission.
            :exceptions: ValueError if compilation fails.
        '''

    def compile_to_binary(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source code into a binary program package.

            :param source: Raw .scara script text.
            :return: BinaryProgram package containing packed binary frames.
            :exceptions: ValueError if parsing or validation fails.
        '''

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL source code directly into a binary wire byte stream.

            :param source: Raw .scara script text.
            :return: Raw byte stream suitable for UART transmission.
            :exceptions: ValueError if compilation fails.
        '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Validated BinaryProgram domain model.
            :exceptions: ValueError if plan contains empty waypoints or invalid geometry.
        '''

    def get_program_telemetry(
        self,
        *,
        program: BinaryProgram
    ) -> BinaryProgramTelemetry:
        '''
            Computes and returns binary program execution metrics and telemetry.

            :param program: BinaryProgram domain model instance.
            :return: BinaryProgramTelemetry metrics domain model.
            :exceptions: None.
        '''

    def get_version(self) -> str:
        '''
            Returns the compiler version string representation.

            :return: Version string representation.
        '''
