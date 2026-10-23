# -*- coding: UTF-8 -*-

'''
Module
    jacobian.py
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
    Defines pure 2x2 Jacobian matrix data model for SCARA planar differential kinematics.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class JacobianMatrix2D:
    '''
        Immutable 2x2 Jacobian matrix data structure for planar SCARA arm calculations.

        It defines:

            :attributes:
                | j11 - Row 1, Column 1 Jacobian coefficient (dx/dtheta1).
                | j12 - Row 1, Column 2 Jacobian coefficient (dx/dtheta2).
                | j21 - Row 2, Column 1 Jacobian coefficient (dy/dtheta1).
                | j22 - Row 2, Column 2 Jacobian coefficient (dy/dtheta2).
    '''

    j11: float
    j12: float
    j21: float
    j22: float
