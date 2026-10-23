# -*- coding: UTF-8 -*-

'''
Module
    axis.py
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
    Defines AxisName enumeration representing SCARA manipulator joint axes.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class AxisName(StrEnum):
    '''
        Enumeration of SCARA manipulator degrees of freedom.

        It defines:

            :attributes:
                | J1 - Primary shoulder joint rotational axis.
                | J2 - Secondary elbow joint rotational axis.
                | Z - Vertical Cartesian linear carriage axis.
                | J4 - Wrist end-effector rotational orientation axis.
    '''

    J1 = 'J1'
    J2 = 'J2'
    Z = 'Z'
    J4 = 'J4'
