# -*- coding: UTF-8 -*-

'''
Module
    itangent_macro_expander.py
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
    Defines structural protocol ITangentMacroExpander for tangent macro expansion and angle computation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITangentMacroExpander(Protocol):
    '''
        Structural protocol defining contract for tangent orientation macro expansion
        and tangent heading angle calculation.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if macro expander applies to given instruction node.
                | expand - Updates tool orientation mode and heading in compiler context.
                | calculate_tangent_angle - Computes tangent heading angle between two 2D points.
    '''

    def can_expand(self, *, instruction: ScaraInstruction) -> bool:
        '''
            Checks whether this expander handles the given instruction type.

            :param instruction: ScaraInstruction node to check.
            :return: True if expander can handle the instruction, False otherwise.
        '''

    def expand(
        self,
        *,
        instruction: ScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[ScaraInstruction, ...]:
        '''
            Configures tool orientation mode in compiler context.

            :param instruction: TOOL_ORIENT instruction node.
            :param context: Active compiler context.
            :return: Empty tuple since orientation configuration mutates context only.
        '''

    def calculate_tangent_angle(
        self,
        *,
        source: Point2D,
        target: Point2D,
        fallback_phi: float,
    ) -> float:
        '''
            Computes tangent heading angle in degrees between two 2D points.

            :param source: Source 2D point coordinates.
            :param target: Destination 2D point coordinates.
            :param fallback_phi: Heading to return if travel distance is zero.
            :return: Heading angle in degrees [-180, +180].
        '''
