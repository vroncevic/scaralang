# -*- coding: UTF-8 -*-

'''
Module
    ibuilder.py
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
    Defines structural protocol IZoneBuilder for constructing obstacle zone domain models.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IZoneBuilder(Protocol):
    '''
        Structural protocol defining construction of ObstacleZone instances from AST instructions.

        It defines:

            :methods:
                | build_zone - Constructs an ObstacleZone from a ZONE_DEF instruction.
                | get_version - Gets implementation version string.
    '''

    def build_zone(
        self,
        *,
        instruction: ScaraInstruction,
    ) -> ObstacleZone:
        '''
            Constructs an ObstacleZone model from parsed instruction parameters.

            :param instruction: ScaraInstruction representing ZONE_DEF command.
            :return: Fully configured ObstacleZone domain instance.
        '''

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
