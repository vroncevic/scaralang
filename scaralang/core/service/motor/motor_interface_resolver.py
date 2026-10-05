# -*- coding: UTF-8 -*-

'''
Module
    motor_interface_resolver.py
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
    Service resolver for motor communication and electrical interface types.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorInterfaceResolver:
    '''
        Service resolving and validating motor communication and electrical interface types.

        It defines:

            :attributes:
                | _INTERFACE_LOOKUP - Dictionary mapping recognized strings to MotorInterfaceType.
            :methods:
                | resolve_interface_type - Resolves and validates interface with mode-aware defaults.
                | supported_interface_strings - Returns tuple of supported interface strings.
                | get_version - Returns resolver version string.
    '''

    _INTERFACE_LOOKUP: ClassVar[dict[str, MotorInterfaceType]] = {
        MotorInterfaceType.STEP_DIR.value: MotorInterfaceType.STEP_DIR,
        MotorInterfaceType.CAN_BUS.value: MotorInterfaceType.CAN_BUS,
        MotorInterfaceType.SERIAL.value: MotorInterfaceType.SERIAL,
    }

    @classmethod
    def resolve_interface_type(
        cls,
        *,
        mode: MotorDriveMode,
        raw_interface: str = '',
    ) -> MotorInterfaceType:
        '''
            Resolves and validates motor interface type with mode-aware defaults.

            :param mode: Actuation drive mode.
            :param raw_interface: Optional raw interface string (e.g. STEP_DIR, CAN_BUS).
            :return: Resolved MotorInterfaceType enum member.
            :exceptions: ScaraSemanticError if raw_interface is invalid.
        '''
        clean: str = raw_interface.strip().upper()

        if clean:
            if clean in cls._INTERFACE_LOOKUP:
                return cls._INTERFACE_LOOKUP[clean]

            raise ScaraSemanticError(
                f'Invalid motor interface {raw_interface!r}. '
                f'Must be one of: {cls.supported_interface_strings()}'
            )

        if mode == MotorDriveMode.CLOSED_LOOP:
            return MotorInterfaceType.CAN_BUS

        return MotorInterfaceType.STEP_DIR

    @classmethod
    def supported_interface_strings(cls) -> tuple[str, ...]:
        '''
            Returns tuple of supported motor interface strings.

            :return: Tuple of supported interface names.
        '''
        return tuple(cls._INTERFACE_LOOKUP.keys())

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns resolver component version.

            :return: Version string.
        '''
        return __version__
