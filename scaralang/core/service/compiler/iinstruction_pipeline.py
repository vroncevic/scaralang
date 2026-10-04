# -*- coding: UTF-8 -*-

'''
Module
    iinstruction_pipeline.py
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
    Defines structural protocol IInstructionPipeline for compiling AST instructions into waypoints.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IInstructionPipeline(Protocol):
    '''
        Structural protocol defining execution pipeline for AST instruction
        expansion and compilation.

        It defines:

            :methods:
                | compile_instructions - Expands and compiles AST instructions into Waypoints.
                | get_version - Returns the instruction pipeline version string.
    '''

    def compile_instructions(
        self,
        *,
        instructions: Sequence[ScaraInstruction],
    ) -> list[Waypoint]:
        '''
            Expands and compiles AST instructions into Waypoint list.

            :param instructions: Sequence of AST ScaraInstruction nodes.
            :return: Mutable list of compiled Waypoint instances.
        '''

    def get_version(self) -> str:
        '''
            Returns the pipeline version string representation.

            :return: Version string representation.
        '''
