# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_compiler.py
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
    Defines interface IScaraDslCompiler for compiling SCARA DSL scripts
    into executable TrajectoryPlans.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.program import ScaraProgram
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
class IScaraDslCompiler(Protocol):
    '''
        Role interface protocol for SCARA DSL compilation.

        It defines:

            :methods:
                | compile_script - Compiles DSL source code into executable ITrajectoryPlan.
                | compile_program - Compiles AST program into executable ITrajectoryPlan.
    '''

    def compile_script(self, *, source: str) -> ITrajectoryPlan:
        '''
            Compiles DSL source code into an executable and validated ITrajectoryPlan.

            :param source: Raw .scara script text.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ValueError if syntax or static analysis errors occur.
        '''

    def compile_program(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles parsed AST program into an executable and validated ITrajectoryPlan.

            :param program: ScaraProgram AST instance to compile.
            :return: Validated ITrajectoryPlan protocol instance.
            :exceptions: ValueError if static analysis errors occur.
        '''
