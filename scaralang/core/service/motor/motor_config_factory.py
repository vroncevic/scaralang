# -*- coding: UTF-8 -*-

'''
Module
    motor_config_factory.py
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
    Factory service instantiating MotorConfig domain models.
'''

from __future__ import annotations

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.motor.motor_config import MotorConfig
from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.motor.motor_interface_type import MotorInterfaceType
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.motor.motor_drive_mode_resolver import MotorDriveModeResolver
from scaralang.core.service.motor.motor_interface_resolver import MotorInterfaceResolver
from scaralang.core.service.motor.motor_wire_mode_converter import MotorWireModeConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorConfigFactory:
    '''
        Factory providing MotorConfig domain instances and delegating mode resolution.

        It defines:

            :methods:
                | create - Creates an instance of MotorConfig with specified parameters.
                | create_open_loop - Creates a default open-loop MotorConfig.
                | create_closed_loop - Creates a default closed-loop MotorConfig.
                | parse_drive_mode - Resolves raw string into MotorDriveMode enum.
                | is_valid_drive_mode - Verifies whether a raw string is a valid drive mode.
                | supported_mode_strings - Returns tuple of all supported drive mode strings.
                | resolve_interface_type - Resolves and validates interface with mode defaults.
                | supported_interface_strings - Returns tuple of supported interface strings.
                | to_wire_mode - Maps domain MotorDriveMode to protocol MotorWireMode.
                | from_wire_mode - Maps wire mode integer or enum to domain MotorDriveMode.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        mode: MotorDriveMode,
        interface_type: MotorInterfaceType,
        axis_mask: AxisMask,
    ) -> MotorConfig:
        '''
            Builds and returns a configured MotorConfig instance.

            :param mode: Actuation drive mode.
            :param interface_type: Communication/electrical interface type.
            :param axis_mask: Target axis bitmask.
            :return: Configured MotorConfig instance.
        '''
        return MotorConfig(
            mode=mode,
            interface_type=interface_type,
            axis_mask=axis_mask,
        )

    @classmethod
    def create_open_loop(
        cls,
        *,
        axis_mask: AxisMask = AxisMask.ALL,
        interface_type: MotorInterfaceType = MotorInterfaceType.STEP_DIR,
    ) -> MotorConfig:
        '''
            Builds a default open-loop MotorConfig instance.

            :param axis_mask: Target axis bitmask (default AxisMask.ALL).
            :param interface_type: Interface type (default MotorInterfaceType.STEP_DIR).
            :return: Configured open-loop MotorConfig instance.
        '''
        return MotorConfig(
            mode=MotorDriveMode.OPEN_LOOP,
            interface_type=interface_type,
            axis_mask=axis_mask,
        )

    @classmethod
    def create_closed_loop(
        cls,
        *,
        axis_mask: AxisMask = AxisMask.ALL,
        interface_type: MotorInterfaceType = MotorInterfaceType.CAN_BUS,
    ) -> MotorConfig:
        '''
            Builds a default closed-loop MotorConfig instance.

            :param axis_mask: Target axis bitmask (default AxisMask.ALL).
            :param interface_type: Interface type (default MotorInterfaceType.CAN_BUS).
            :return: Configured closed-loop MotorConfig instance.
        '''
        return MotorConfig(
            mode=MotorDriveMode.CLOSED_LOOP,
            interface_type=interface_type,
            axis_mask=axis_mask,
        )

    @classmethod
    def parse_drive_mode(cls, mode_val: str) -> MotorDriveMode:
        '''
            Parses raw string representation into MotorDriveMode enum.

            :param mode_val: Raw motor mode string.
            :return: Matching MotorDriveMode enum member.
            :exceptions: ValueError if raw string is not recognized.
        '''
        return MotorDriveModeResolver.parse_drive_mode(mode_val)

    @classmethod
    def is_valid_drive_mode(cls, mode_val: str) -> bool:
        '''
            Checks whether raw string represents a supported motor drive mode.

            :param mode_val: Raw motor mode string.
            :return: True if valid, False otherwise.
        '''
        return MotorDriveModeResolver.is_valid_drive_mode(mode_val)

    @classmethod
    def supported_mode_strings(cls) -> tuple[str, ...]:
        '''
            Returns tuple of all recognized motor drive mode strings.

            :return: Tuple of supported mode string representations.
        '''
        return MotorDriveModeResolver.supported_mode_strings()

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
            :exceptions: ValueError if raw_interface is invalid.
        '''
        return MotorInterfaceResolver.resolve_interface_type(
            mode=mode, raw_interface=raw_interface
        )

    @classmethod
    def supported_interface_strings(cls) -> tuple[str, ...]:
        '''
            Returns tuple of supported motor interface strings.

            :return: Tuple of supported interface names.
        '''
        return MotorInterfaceResolver.supported_interface_strings()

    @classmethod
    def to_wire_mode(cls, mode: MotorDriveMode) -> MotorWireMode:
        '''
            Maps domain MotorDriveMode to binary wire protocol MotorWireMode.

            :param mode: Domain MotorDriveMode enum.
            :return: Corresponding MotorWireMode.
        '''
        return MotorWireModeConverter.to_wire_mode(mode)

    @classmethod
    def from_wire_mode(cls, wire_mode: int | MotorWireMode) -> MotorDriveMode:
        '''
            Maps wire protocol integer or enum value to domain MotorDriveMode.

            :param wire_mode: Wire mode integer or MotorWireMode enum.
            :return: Corresponding MotorDriveMode.
        '''
        return MotorWireModeConverter.from_wire_mode(wire_mode)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version.

            :return: Version string.
        '''
        return __version__
