# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan_compiler.py
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
    Defines structural runtime-checkable protocol ITrajectoryPlanCompiler.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryPlanCompiler(Protocol):
    '''
        Structural protocol defining contract for compiling SCARA AST programs into plans.

        It defines:

            :methods:
                | compile - Compiles ScaraProgram into validated ITrajectoryPlan.
                | get_version - Returns the compiler version string.
    '''

    def compile(self, *, program: ScaraProgram) -> ITrajectoryPlan:
        '''
            Compiles a SCARA DSL program into an executable and validated ITrajectoryPlan.

            :param program: Parsed ScaraProgram AST root.
            :return: Validated ITrajectoryPlan instance.
        '''

    def get_version(self) -> str:
        '''
            Returns the compiler version string representation.

            :return: Version string representation.
        '''
