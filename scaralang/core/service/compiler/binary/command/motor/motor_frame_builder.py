# -*- coding: UTF-8 -*-

'''
Module
    motor_frame_builder.py
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
    Implementation of IMotorFrameBuilder constructing motor configuration binary frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.motor.motor_drive_mode import MotorDriveMode
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.motor_wire_mode import MotorWireMode
from scaralang.core.service.motor.motor_config_factory import MotorConfigFactory
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotorFrameBuilder:
    '''
        Constructs binary wire frames for motor actuation mode configuration.

        It defines:

            :attributes:
                | _frame_builder - Injected binary frame builder protocol.
            :methods:
                | __init__ - Initializes motor frame builder with wire frame builder.
                | build_motor_frame - Constructs binary frame for motor configuration.
                | get_version - Gets implementation version string.
    '''

    _frame_builder: IBinaryFrameBuilder

    def __init__(self, *, frame_builder: IBinaryFrameBuilder) -> None:
        '''
            Initializes MotorFrameBuilder with injected frame builder.

            :param frame_builder: Low-level binary frame builder protocol.
        '''
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder

    def build_motor_frame(
        self,
        *,
        arg: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Constructs binary frame for motor drive mode configuration.

            :param arg: Command argument string.
            :param seq_num: Frame sequence counter.
            :return: Instantiated BinaryFrame.
            :exceptions: None.
        '''
        drive_mode: MotorDriveMode = (
            MotorConfigFactory.parse_drive_mode(arg)
            if arg and MotorConfigFactory.is_valid_drive_mode(arg)
            else MotorDriveMode.OPEN_LOOP
        )
        wire_mode: MotorWireMode = MotorConfigFactory.to_wire_mode(drive_mode)

        return self._frame_builder.build_motor_config_cmd(
            seq_num=seq_num,
            mode=wire_mode.value,
        )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
