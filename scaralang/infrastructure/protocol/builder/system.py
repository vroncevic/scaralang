# -*- coding: UTF-8 -*-

'''
Module
    system.py
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
    Concrete implementation of binary system and control command frame builder.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar, Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinarySystemFrameBuilder:
    '''
        Builds system and control binary frames using injected wire frame packer.

        It defines:

            :attributes:
                | DEFAULT_JOG_SPEED - Default stepping rate for jog motion (2000).
                | MIN_OVERRIDE_PERCENT - Minimum execution speed override (1%).
                | MAX_OVERRIDE_PERCENT - Maximum execution speed override (200%).
                | BYTE_MASK - Bitmask isolating single byte values (0xFF).
                | WAIT_FORMAT - Struct format for 4-byte wait delay payload.
                | JOG_FORMAT - Struct format for 9-byte joint jog payload.
                | OVERRIDE_FORMAT - Struct format for 1-byte speed override payload.
                | _packer - Injected wire frame packer service port.
            :methods:
                | __init__ - Initializes builder with wire frame packer collaborator.
                | build_system_cmd - Builds parameterless system command.
                | build_wait_cmd - Builds a delay pause command frame.
                | build_jog_frame - Builds a single joint relative jog frame.
                | build_override_frame - Builds an execution speed override command frame.
                | get_version - Returns component version string.
    '''

    DEFAULT_JOG_SPEED: ClassVar[int] = 2000
    MIN_OVERRIDE_PERCENT: ClassVar[int] = 1
    MAX_OVERRIDE_PERCENT: ClassVar[int] = 200
    BYTE_MASK: ClassVar[int] = 0xFF
    WAIT_FORMAT: ClassVar[str] = str(BinaryStructFormat.WAIT)
    JOG_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOG)
    OVERRIDE_FORMAT: ClassVar[str] = str(BinaryStructFormat.OVERRIDE)

    _packer: IBinaryFramePacker

    def __init__(self, *, packer: IBinaryFramePacker) -> None:
        '''
            Initializes system frame builder with wire frame packer port.

            :param packer: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._packer: Final[IBinaryFramePacker] = packer

    def build_system_cmd(
        self,
        *,
        msg_id: MessageId,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Builds a parameterless system command frame (ENABLE, ESTOP, PING, etc.).

            :param msg_id: Target command message identifier.
            :param seq_num: Cyclic sequence index.
            :return: Assembled parameterless BinaryFrame.
            :exceptions: None.
        '''
        return self._packer.build_frame(msg_id=msg_id, seq_num=seq_num, payload=b'')

    def build_wait_cmd(self, *, delay_ms: int, seq_num: int) -> BinaryFrame:
        '''
            Builds a delay pause command frame (CMD_WAIT).

            :param delay_ms: Dwell duration in milliseconds.
            :param seq_num: Cyclic sequence index.
            :return: Assembled BinaryFrame with packed delay payload.
            :exceptions: None.
        '''
        payload: bytes = pack(self.WAIT_FORMAT, max(0, delay_ms))

        return self._packer.build_frame(
            msg_id=MessageId.CMD_WAIT,
            seq_num=seq_num,
            payload=payload,
        )

    def build_jog_frame(
        self,
        *,
        seq_num: int,
        joint_id: int,
        step: int,
        speed: int = DEFAULT_JOG_SPEED,
    ) -> BinaryFrame:
        '''
            Builds a single joint relative jog frame.

            :param seq_num: Cyclic sequence index.
            :param joint_id: Joint index (0: J1, 1: J2, 2: Z, 3: J4).
            :param step: Relative step count displacement.
            :param speed: Target stepping speed in steps per second.
            :return: Assembled BinaryFrame with CMD_JOG_JOINT payload.
            :exceptions: None.
        '''
        payload: bytes = pack(
            self.JOG_FORMAT,
            joint_id & self.BYTE_MASK,
            step,
            speed,
        )

        return self._packer.build_frame(
            msg_id=MessageId.CMD_JOG_JOINT,
            seq_num=seq_num,
            payload=payload,
        )

    def build_override_frame(self, *, seq_num: int, pct: int) -> BinaryFrame:
        '''
            Builds an execution speed override command frame.

            :param seq_num: Cyclic sequence index.
            :param pct: Speed override percentage (1 to 200).
            :return: Assembled BinaryFrame with CMD_OVERRIDE payload.
            :exceptions: None.
        '''
        clamped_pct: int = max(
            self.MIN_OVERRIDE_PERCENT, min(self.MAX_OVERRIDE_PERCENT, pct)
        )
        payload: bytes = pack(self.OVERRIDE_FORMAT, clamped_pct)

        return self._packer.build_frame(
            msg_id=MessageId.CMD_OVERRIDE,
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
