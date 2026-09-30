# -*- coding: UTF-8 -*-

'''
Module
    motor_wire_mode.py
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
    Defines MotorWireMode enumeration for motor drive mode wire protocol encoding.
'''

from __future__ import annotations

from enum import IntEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class MotorWireMode(IntEnum):
    '''
        Enumeration of motor drive mode wire representation values.

        It defines:

            :attributes:
                | OPEN_LOOP - Open-loop drive wire value (0).
                | CLOSED_LOOP - Closed-loop drive wire value (1).
    '''

    OPEN_LOOP = 0
    CLOSED_LOOP = 1
