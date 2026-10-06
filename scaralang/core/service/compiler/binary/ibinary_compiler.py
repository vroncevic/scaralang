# -*- coding: UTF-8 -*-

'''
Module
    ibinary_compiler.py
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
    Defines IBinaryCompiler Protocol for compiling trajectory plans into binary programs.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.program import BinaryProgram
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
class IBinaryCompiler(Protocol):
    '''
        Structural protocol defining contracts for compiling trajectory plans into binary programs.

        It defines:

            :methods:
                | compile_plan - Compiles ITrajectoryPlan into BinaryProgram package.
                | get_version - Gets implementation version string.
    '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> BinaryProgram:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: Validated ITrajectoryPlan protocol instance.
            :return: Compiled BinaryProgram containing binary frames and byte stream.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
