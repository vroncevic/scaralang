# -*- coding: UTF-8 -*-

'''
Module
    actuator.py
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
    Concrete implementation of binary actuator and tool frame builder.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar, Final

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.protocol.ibinary_frame_packer import IBinaryFramePacker
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryActuatorFrameBuilder:
    '''
        Builds tool and motor configuration binary frames using injected wire frame packer.

        It defines:

            :attributes:
                | BYTE_MASK - Bitmask isolating single byte values (0xFF).
                | TOOL_CMD_FORMAT - Struct format for 2-byte tool actuation payload.
                | CONFIG_MOTOR_FORMAT - Struct format for 2-byte motor config payload.
                | _packer - Injected wire frame packer service port.
            :methods:
                | __init__ - Initializes builder with wire frame packer collaborator.
                | build_tool_cmd - Builds tool state actuation frame.
                | build_motor_config_cmd - Builds motor configuration frame.
                | get_version - Returns component version string.
    '''

    BYTE_MASK: ClassVar[int] = 0xFF
    TOOL_CMD_FORMAT: ClassVar[str] = str(BinaryStructFormat.TOOL_CMD)
    CONFIG_MOTOR_FORMAT: ClassVar[str] = str(BinaryStructFormat.CONFIG_MOTOR)

    _packer: IBinaryFramePacker

    def __init__(self, *, packer: IBinaryFramePacker) -> None:
        '''
            Initializes actuator frame builder with wire frame packer port.

            :param packer: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._packer: Final[IBinaryFramePacker] = packer

    def build_tool_cmd(
        self,
        *,
        seq_num: int,
        tool_id: int,
        state: bool,
    ) -> BinaryFrame:
        '''
            Builds a tool actuation command frame (PUMP, VALVE).

            :param seq_num: Cyclic sequence index.
            :param tool_id: Tool identifier (0=PUMP, 1=VALVE).
            :param state: True to activate, False to deactivate.
            :return: Assembled tool command BinaryFrame.
            :exceptions: None.
        '''
        target_cmd: MessageId = (
            MessageId.CMD_TOOL_PUMP if tool_id == ToolId.PUMP else MessageId.CMD_TOOL_VALVE
        )
        tool_payload: bytes = pack(
            self.TOOL_CMD_FORMAT, tool_id & self.BYTE_MASK, 1 if state else 0
        )

        return self._packer.build_frame(
            msg_id=target_cmd,
            seq_num=seq_num,
            payload=tool_payload,
        )

    def build_motor_config_cmd(
        self,
        *,
        seq_num: int,
        mode: int,
        axis_mask: int = AxisMask.ALL,
    ) -> BinaryFrame:
        '''
            Builds a motor actuation mode configuration frame.

            :param seq_num: Cyclic sequence index.
            :param mode: Motor drive mode integer (0=OPEN_LOOP, 1=CLOSED_LOOP).
            :param axis_mask: Bitmask of target axes (default AxisMask.ALL).
            :return: Assembled motor configuration BinaryFrame.
            :exceptions: None.
        '''
        payload: bytes = pack(
            self.CONFIG_MOTOR_FORMAT, mode & self.BYTE_MASK, axis_mask & self.BYTE_MASK
        )

        return self._packer.build_frame(
            msg_id=MessageId.CMD_CONFIG_MOTOR,
            seq_num=seq_num,
            payload=payload,
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
