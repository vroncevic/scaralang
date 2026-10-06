# -*- coding: UTF-8 -*-

'''
Module
    iscara_plan_compiler.py
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
    Defines structural runtime-checkable protocol IScaraPlanCompiler for compiling
    SCARA DSL scripts into executable and validated trajectory plans.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraPlanCompiler(Protocol):
    '''
        Structural protocol defining contract for compiling SCARA DSL scripts into plans.

        It defines:

            :methods:
                | compile - Compiles DSL source code into validated ITrajectoryPlan.
                | compile_script - Compiles DSL source code into validated ITrajectoryPlan.
                | compile_program - Compiles AST program into validated ITrajectoryPlan.
                | get_version - Returns the plan compiler version string.
    '''

    def compile(self, *, source: str) -> ITrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated ITrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions:
                | ScaraSyntaxError: If script contains invalid syntax.
                | ScaraSemanticError: If static analysis diagnostics occur.
        '''

    def compile_script(self, *, source: str) -> ITrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated ITrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions:
                | ScaraSyntaxError: If script contains invalid syntax.
                | ScaraSemanticError: If static analysis diagnostics occur.
        '''

    def compile_program(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles a parsed AST program into an executable and validated ITrajectoryPlan.

            :param program: Parsed ScaraProgram AST instance to compile.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions:
                | ScaraSemanticError: If AST validation fails.
        '''

    def get_version(self) -> str:
        '''
            Returns the plan compiler version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
