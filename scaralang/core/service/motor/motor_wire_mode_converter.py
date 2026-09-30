# -*- coding: UTF-8 -*-

'''
Module
    motor_wire_mode_converter.py
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
    Service converting between domain MotorDriveMode and binary wire MotorWireMode.
'''

from __future__ import annotations

from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorWireModeConverter:
    '''
        Service converting between domain MotorDriveMode and wire protocol MotorWireMode.

        It defines:

            :methods:
                | to_wire_mode - Maps domain MotorDriveMode to protocol MotorWireMode.
                | from_wire_mode - Maps wire mode integer or enum to domain MotorDriveMode.
                | get_version - Returns converter version string.
    '''

    @classmethod
    def to_wire_mode(cls, mode: MotorDriveMode) -> MotorWireMode:
        '''
            Maps domain MotorDriveMode to binary wire protocol MotorWireMode.

            :param mode: Domain MotorDriveMode enum.
            :return: Corresponding MotorWireMode.
        '''
        if mode == MotorDriveMode.CLOSED_LOOP:
            return MotorWireMode.CLOSED_LOOP

        return MotorWireMode.OPEN_LOOP

    @classmethod
    def from_wire_mode(cls, wire_mode: int | MotorWireMode) -> MotorDriveMode:
        '''
            Maps wire protocol integer or enum value to domain MotorDriveMode.

            :param wire_mode: Wire mode integer or MotorWireMode enum.
            :return: Corresponding MotorDriveMode.
        '''
        if wire_mode in (MotorWireMode.CLOSED_LOOP, MotorWireMode.CLOSED_LOOP.value):
            return MotorDriveMode.CLOSED_LOOP

        return MotorDriveMode.OPEN_LOOP

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns converter component version.

            :return: Version string.
        '''
        return __version__
