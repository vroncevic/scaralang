# -*- coding: UTF-8 -*-

'''
Module
    motor_drive_mode_resolver.py
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
    Service resolver for motor actuation drive modes.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_drive_mode_alias import MotorDriveModeAlias
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorDriveModeResolver:
    '''
        Service parsing, normalizing, and validating motor actuation drive modes.

        It defines:

            :attributes:
                | _MODE_LOOKUP - Dictionary mapping recognized mode strings to MotorDriveMode.
            :methods:
                | parse_drive_mode - Resolves raw string into MotorDriveMode enum.
                | is_valid_drive_mode - Verifies whether a raw string is a valid drive mode.
                | supported_mode_strings - Returns tuple of all supported drive mode strings.
                | get_version - Returns resolver version string.
    '''

    _MODE_LOOKUP: ClassVar[dict[str, MotorDriveMode]] = {
        MotorDriveMode.OPEN_LOOP.value: MotorDriveMode.OPEN_LOOP,
        MotorDriveMode.CLOSED_LOOP.value: MotorDriveMode.CLOSED_LOOP,
        MotorDriveModeAlias.OPEN.value: MotorDriveMode.OPEN_LOOP,
        MotorDriveModeAlias.CLOSED.value: MotorDriveMode.CLOSED_LOOP,
        str(int(MotorWireMode.OPEN_LOOP)): MotorDriveMode.OPEN_LOOP,
        str(int(MotorWireMode.CLOSED_LOOP)): MotorDriveMode.CLOSED_LOOP,
    }

    @classmethod
    def parse_drive_mode(cls, mode_val: str) -> MotorDriveMode:
        '''
            Parses raw string representation into MotorDriveMode enum.

            :param mode_val: Raw motor mode string.
            :return: Matching MotorDriveMode enum member.
            :exceptions: ScaraSemanticError if raw string is not recognized.
        '''
        normalized: str = mode_val.strip().upper()

        if normalized in cls._MODE_LOOKUP:
            return cls._MODE_LOOKUP[normalized]

        raise ScaraSemanticError(
            f'Invalid motor drive mode {mode_val!r}. '
            f'Must be one of: {cls.supported_mode_strings()}'
        )

    @classmethod
    def is_valid_drive_mode(cls, mode_val: str) -> bool:
        '''
            Checks whether raw string represents a supported motor drive mode.

            :param mode_val: Raw motor mode string.
            :return: True if valid, False otherwise.
        '''
        return mode_val.strip().upper() in cls._MODE_LOOKUP

    @classmethod
    def supported_mode_strings(cls) -> tuple[str, ...]:
        '''
            Returns tuple of all recognized motor drive mode strings.

            :return: Tuple of supported mode string representations.
        '''
        return tuple(cls._MODE_LOOKUP.keys())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns resolver component version.

            :return: Version string.
        '''
        return __version__
