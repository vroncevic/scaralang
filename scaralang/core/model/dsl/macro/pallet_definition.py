# -*- coding: UTF-8 -*-

'''
Module
    pallet_definition.py
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
    Immutable domain model representing a pallet matrix layout definition.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.kinematics.point_2d import Point2D

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class PalletDefinition:
    '''
        Immutable domain entity representing a pallet matrix layout in local work coordinates.

        It defines:

            :attributes:
                | name - Identifier name of the pallet matrix.
                | rows - Number of grid rows in the pallet matrix.
                | cols - Number of grid columns in the pallet matrix.
                | dx - Column spacing pitch in millimeters.
                | dy - Row spacing pitch in millimeters.
                | start - Origin coordinate Point2D of cell index 0 in millimeters.
    '''

    name: str
    rows: int
    cols: int
    dx: float
    dy: float
    start: Point2D
