# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.service.compiler.binary.icompiler import IBinaryCompiler
from scaralang.core.service.compiler.plan.script.icompiler import IScriptPlanCompiler
from scaralang.core.service.trajectory.plan.iplan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraCompiler:
    '''
        Compiler service implementing binary frame compilation for SCARA DSL.

        It defines:

            :attributes:
                | _compiler - DSL plan compiler protocol instance.
                | _binary_compiler - Trajectory plan to binary compiler protocol instance.
            :methods:
                | __init__ - Initializes compiler with injected collaborators.
                | compile - Compiles DSL source text into BinaryProgram package.
                | compile_bytes - Compiles DSL source code into raw UART byte stream.
                | get_version - Returns compiler version string.
    '''

    _compiler: IScriptPlanCompiler
    _binary_compiler: IBinaryCompiler

    def __init__(
        self,
        *,
        compiler: IScriptPlanCompiler,
        binary_compiler: IBinaryCompiler,
    ) -> None:
        '''
            Initializes ScaraCompiler with required compiler delegates.

            :param compiler: Required IScriptPlanCompiler protocol instance.
            :param binary_compiler: Required IBinaryCompiler protocol instance.
            :exceptions: None.
        '''
        self._compiler: Final[IScriptPlanCompiler] = compiler
        self._binary_compiler: Final[IBinaryCompiler] = binary_compiler

    def compile(self, *, source: str) -> BinaryProgram:
        '''
            Compiles DSL source code into a binary program package.

            :param source: Raw .scara script text.
            :return: BinaryProgram package containing packed binary frames.
            :exceptions: ValueError if parsing or validation fails.
        '''
        plan: ITrajectoryPlan = self._compiler.compile_script(source=source)

        return self._binary_compiler.compile_plan(plan=plan)

    def compile_bytes(self, *, source: str) -> bytes:
        '''
            Compiles DSL source code directly into a binary wire byte stream.

            :param source: Raw .scara script text.
            :return: Raw byte stream suitable for UART transmission.
            :exceptions: ValueError if compilation fails.
        '''
        program: BinaryProgram = self.compile(source=source)

        return program.raw_bytes

    def get_version(self) -> str:
        '''
        Returns the compiler version string representation.

        :return: Version string representation.
        :exceptions: None.
        '''
        return __version__
