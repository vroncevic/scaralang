# -*- coding: UTF-8 -*-

'''
Module
    builder.py
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
    Implementation of ActuatorFrameBuilder constructing actuator configuration binary frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.motor.drive_mode_resolver import DriveModeResolver
from scaralang.core.service.motor.wire_mode_converter import WireModeConverter
from scaralang.core.service.protocol.ibinary_actuator_frame_builder import IBinaryActuatorFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ActuatorFrameBuilder:
    '''
        Constructs binary wire frames for actuator actuation mode configuration.

        It defines:

            :attributes:
                | _frame_builder - Injected actuator binary frame builder protocol.
            :methods:
                | __init__ - Initializes actuator frame builder with wire frame builder.
                | build_actuator_frame - Constructs binary frame for actuator configuration.
                | build_motor_frame - Compatibility alias constructing actuator frame.
                | get_version - Gets implementation version string.
    '''

    _frame_builder: IBinaryActuatorFrameBuilder

    def __init__(self, *, frame_builder: IBinaryActuatorFrameBuilder) -> None:
        '''
            Initializes ActuatorFrameBuilder with injected frame builder.

            :param frame_builder: Low-level actuator binary frame builder protocol.
        '''
        self._frame_builder: Final[IBinaryActuatorFrameBuilder] = frame_builder

    def build_actuator_frame(
        self,
        *,
        arg: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Constructs binary frame for actuator drive mode configuration.

            :param arg: Command argument string.
            :param seq_num: Frame sequence counter.
            :return: Instantiated BinaryFrame.
            :exceptions: None.
        '''
        drive_mode: MotorDriveMode = (
            DriveModeResolver.parse_drive_mode(arg)
            if arg and DriveModeResolver.is_valid_drive_mode(arg)
            else MotorDriveMode.OPEN_LOOP
        )
        wire_mode: MotorWireMode = WireModeConverter.to_wire_mode(drive_mode)

        return self._frame_builder.build_motor_config_cmd(
            seq_num=seq_num,
            mode=wire_mode.value,
        )

    def build_motor_frame(
        self,
        *,
        arg: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Compatibility alias constructing binary frame for actuator configuration.

            :param arg: Command argument string.
            :param seq_num: Frame sequence counter.
            :return: Instantiated BinaryFrame.
            :exceptions: None.
        '''
        return self.build_actuator_frame(arg=arg, seq_num=seq_num)

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
