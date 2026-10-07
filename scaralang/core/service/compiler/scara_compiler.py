# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler.py
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
    Implementation of IScaraCompiler orchestrating DSL parsing and binary frame compilation.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.plan.iscara_plan_compiler import IScaraPlanCompiler
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompiler:
    '''
        Compiler service implementing binary frame compilation and telemetry for SCARA DSL.

        It defines:

            :attributes:
                | _compiler - DSL plan compiler protocol instance.
                | _binary_compiler - Trajectory plan to binary compiler protocol instance.
            :methods:
                | __init__ - Initializes compiler with injected collaborators.
                | compile - Compiles DSL source text into BinaryProgram package.
                | compile_bytes - Compiles DSL source code into raw UART byte stream.
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | compile_to_binary - Compiles DSL source text into BinaryProgram package.
                | compile_to_bytes - Compiles DSL code directly to raw UART byte stream.
                | get_program_telemetry - Returns execution metrics and telemetry
                  for binary program.
                | get_version - Returns compiler version string.
    '''

    _compiler: IScaraPlanCompiler
    _binary_compiler: IBinaryCompiler

    def __init__(
        self,
        *,
        compiler: IScaraPlanCompiler,
        binary_compiler: IBinaryCompiler,
    ) -> None:
        '''
            Initializes ScaraCompiler with required compiler delegates.

            :param compiler: Required IScaraPlanCompiler protocol instance.
            :param binary_compiler: Required IBinaryCompiler protocol instance.
            :exceptions: None.
        '''
        self._compiler: Final[IScaraPlanCompiler] = compiler
        self._binary_compiler: Final[IBinaryCompiler] = binary_compiler

    def compile(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source code into a binary program package.

            :param source: Raw .scara script text.
            :return: BinaryProgram package containing packed binary frames.
            :exceptions: ValueError if parsing or validation fails.
        '''
        return self.compile_to_binary(source=source)

    def compile_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL source code directly into a binary wire byte stream.

            :param source: Raw .scara script text.
            :return: Raw byte stream suitable for UART transmission.
            :exceptions: ValueError if compilation fails.
        '''
        return self.compile_to_bytes(source=source)

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Validated BinaryProgram domain model.
            :exceptions: ValueError if plan contains empty waypoints or invalid geometry.
        '''
        return self._binary_compiler.compile_plan(plan=plan)

    def compile_to_binary(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source code into a binary program package.

            :param source: Raw .scara script text.
            :return: BinaryProgram package containing packed binary frames.
            :exceptions: ValueError if parsing or validation fails.
        '''
        plan: ITrajectoryPlan = self._compiler.compile_script(source=source)
        return self._binary_compiler.compile_plan(plan=plan)

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL source code directly into a binary wire byte stream.

            :param source: Raw .scara script text.
            :return: Raw byte stream suitable for UART transmission.
            :exceptions: ValueError if compilation fails.
        '''
        program: BinaryProgram = self.compile_to_binary(source=source)
        return program.raw_bytes

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
        return program.telemetry

    def get_version(self) -> str:
        '''
            Returns the compiler version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
