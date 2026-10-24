# -*- coding: UTF-8 -*-

'''
Module
    calculator.py
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
    Service computing disassembly summary metrics from decoded frames.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.disassembler.disassembled_frame import DisassembledFrame
from scaralang.core.model.disassembler.disassembly_summary import DisassemblySummary
from scaralang.core.model.protocol.message import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DisassemblySummaryCalculator:
    '''
        Computes disassembly summary metrics from decoded frames.

        It defines:

            :attributes:
                | _MOTION_MSG_IDS - Set of numeric message IDs categorized as motion commands.
                | _TOOL_MSG_IDS - Set of numeric message IDs categorized as tool commands.
                | _WAIT_MSG_ID - Numeric message ID for wait dwell delay command.
            :methods:
                | __init__ - Initializes calculator instance.
                | calculate_summary - Computes DisassemblySummary domain model.
                | get_version - Returns calculator version string.
    '''

    _MOTION_MSG_IDS: ClassVar[frozenset[int]] = frozenset({
        int(MessageId.CMD_MOVE_JOINT_STEPS),
        int(MessageId.CMD_JOG_JOINT),
        int(MessageId.CMD_SETPOS_STEPS),
    })
    _TOOL_MSG_IDS: ClassVar[frozenset[int]] = frozenset({
        int(MessageId.CMD_TOOL_PUMP),
        int(MessageId.CMD_TOOL_VALVE),
    })
    _WAIT_MSG_ID: ClassVar[int] = int(MessageId.CMD_WAIT)

    def __init__(self) -> None:
        '''
            Initializes calculator instance.

            :exceptions: None.
        '''

    def calculate_summary(
        self,
        *,
        frames: tuple[DisassembledFrame, ...],
        byte_count: int
    ) -> DisassemblySummary:
        '''
            Computes DisassemblySummary domain model from decoded frames and total bytes.

            :param frames: Decoded DisassembledFrame domain models.
            :param byte_count: Total raw bytes parsed from binary source.
            :return: Computed DisassemblySummary domain model.
            :exceptions: None.
        '''
        motion_count: int = sum(
            1 for item in frames
            if item.msg_id in self._MOTION_MSG_IDS
        )
        tool_count: int = sum(
            1 for item in frames
            if item.msg_id in self._TOOL_MSG_IDS
        )
        wait_count: int = sum(
            1 for item in frames
            if item.msg_id == self._WAIT_MSG_ID
        )
        system_count: int = len(frames) - motion_count - tool_count - wait_count

        return DisassemblySummary(
            total_bytes=byte_count,
            decoded_frames=len(frames),
            motion_frames=motion_count,
            tool_commands=tool_count,
            wait_delays=wait_count,
            system_frames=system_count,
        )

    def get_version(self) -> str:
        '''
            Returns the calculator version string.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
