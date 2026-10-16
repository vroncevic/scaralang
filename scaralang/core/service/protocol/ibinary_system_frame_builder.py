# -*- coding: UTF-8 -*-

'''
Module
    ibinary_system_frame_builder.py
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
    Defines IBinarySystemFrameBuilder protocol for system and control command frame construction.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinarySystemFrameBuilder(Protocol):
    '''
        Structural protocol defining system and control binary frame construction contracts.

        It defines:

            :methods:
                | build_system_cmd - Builds a parameterless system command frame.
                | build_wait_cmd - Builds a delay dwell pause command frame.
                | build_jog_frame - Builds a single joint relative jog frame.
                | build_override_frame - Builds an execution speed override command frame.
                | get_version - Returns system frame builder version string.
    '''

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
        '''

    def build_wait_cmd(self, *, delay_ms: int, seq_num: int) -> BinaryFrame:
        '''
            Builds a delay dwell command frame (CMD_WAIT).

            :param delay_ms: Dwell duration in milliseconds.
            :param seq_num: Cyclic sequence index.
            :return: Assembled BinaryFrame with packed delay payload.
        '''

    def build_jog_frame(
        self,
        *,
        seq_num: int,
        joint_id: int,
        step: int,
        speed: int = 2000,
    ) -> BinaryFrame:
        '''
            Builds a single joint relative jog frame (CMD_JOG_JOINT).

            :param seq_num: Cyclic sequence index.
            :param joint_id: Joint index (0: J1, 1: J2, 2: Z, 3: J4).
            :param step: Relative step count displacement.
            :param speed: Target stepping speed in steps per second.
            :return: Assembled BinaryFrame with packed jog payload.
        '''

    def build_override_frame(self, *, seq_num: int, pct: int) -> BinaryFrame:
        '''
            Builds an execution speed override command frame (CMD_OVERRIDE).

            :param seq_num: Cyclic sequence index.
            :param pct: Speed override percentage.
            :return: Assembled BinaryFrame with packed override payload.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
