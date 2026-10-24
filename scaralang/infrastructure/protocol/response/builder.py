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
    Concrete implementation of binary wire response frame builder.
'''

from __future__ import annotations

from struct import pack
from typing import Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.status import ManipulatorStatus
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.model.protocol.event import MoveEventType
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


class BinaryResponseBuilder:
    '''
        Builder constructing binary wire response frames using injected frame packer.

        It defines:

            :attributes:
                | _packer - Injected binary wire frame packer service.
            :methods:
                | __init__ - Initializes builder with binary frame packer collaborator.
                | build_ack - Assembles positive acknowledgment response frame.
                | build_nack - Assembles negative rejection response frame.
                | build_status - Assembles consolidated manipulator telemetry response frame.
                | build_move_event - Assembles motion execution event response frame.
                | get_version - Returns response builder version string.
    '''

    _packer: IBinaryFramePacker

    def __init__(self, *, packer: IBinaryFramePacker) -> None:
        '''
            Initializes response builder with binary frame packer port.

            :param packer: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._packer: Final[IBinaryFramePacker] = packer

    def build_ack(
        self,
        *,
        cmd_id: MessageId,
        seq_num: int,
        free_slots: int,
    ) -> BinaryFrame:
        '''
            Constructs an ACK response frame for an executed command.

            :param cmd_id: MessageId of acknowledged command.
            :param seq_num: Cyclic sequence index matching inbound frame.
            :param free_slots: Available queue capacity slots.
            :return: Assembled BinaryFrame with packed ACK payload.
            :exceptions: None.
        '''
        payload: bytes = pack(BinaryStructFormat.ACK, int(cmd_id), free_slots)

        return self._packer.build_frame(
            msg_id=MessageId.RESP_ACK,
            seq_num=seq_num,
            payload=payload,
        )

    def build_nack(
        self,
        *,
        cmd_id: MessageId,
        seq_num: int,
        error_code: int,
    ) -> BinaryFrame:
        '''
            Constructs a NACK rejection response frame for a failed command.

            :param cmd_id: MessageId of rejected command.
            :param seq_num: Cyclic sequence index matching inbound frame.
            :param error_code: Error reason code.
            :return: Assembled BinaryFrame with packed NACK payload.
            :exceptions: None.
        '''
        payload: bytes = pack(BinaryStructFormat.NACK, int(cmd_id), error_code)

        return self._packer.build_frame(
            msg_id=MessageId.RESP_NACK,
            seq_num=seq_num,
            payload=payload,
        )

    def build_status(
        self,
        *,
        seq_num: int,
        status: ManipulatorStatus,
    ) -> BinaryFrame:
        '''
            Constructs a STATUS telemetry response frame with motor step positions.

            :param seq_num: Cyclic sequence index matching inbound frame.
            :param status: Consolidated manipulator telemetry state model.
            :return: Assembled BinaryFrame with packed STATUS payload.
            :exceptions: None.
        '''
        payload: bytes = pack(
            BinaryStructFormat.STATUS,
            status.system_state,
            1 if status.is_busy else 0,
            status.queue_count,
            status.j1_steps,
            status.j2_steps,
            status.z_steps,
            status.j4_steps,
        )

        return self._packer.build_frame(
            msg_id=MessageId.RESP_STATUS,
            seq_num=seq_num,
            payload=payload,
        )

    def build_move_event(
        self,
        *,
        seq_num: int,
        event_type: MoveEventType | int,
    ) -> BinaryFrame:
        '''
            Constructs a RESP_MOVE_EVENT binary motion notification frame.

            :param seq_num: Cyclic sequence index matching inbound frame.
            :param event_type: Motion event code (MoveEventType or integer).
            :return: Assembled BinaryFrame with packed MOVE_EVENT payload.
            :exceptions: None.
        '''
        event_code: int = (
            event_type.value if isinstance(event_type, MoveEventType) else event_type
        )
        payload: bytes = pack(BinaryStructFormat.MOVE_EVENT, event_code, seq_num)

        return self._packer.build_frame(
            msg_id=MessageId.RESP_MOVE_EVENT,
            seq_num=seq_num,
            payload=payload,
        )

    def get_version(self) -> str:
        '''
            Returns the response builder version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
