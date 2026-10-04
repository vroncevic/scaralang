# -*- coding: UTF-8 -*-

'''
Module
    ibinary_frame_builder.py
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
    Defines IBinaryFrameBuilder interface for packaging binary wire frames.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryFrameBuilder(Protocol):
    '''
        Structural protocol defining binary frame construction contracts.

        It defines:

            :attributes:
                | name - Identifier name of the binary frame builder.
            :methods:
                | build_frame - Assembles a generic binary frame with CRC16.
                | build_joint_move - Builds a MSG_CMD_MOVE_JOINT_STEPS motion frame.
                | build_system_cmd - Builds a parameterless system command frame.
                | build_tool_cmd - Builds a tool actuation command frame.
                | build_motor_config_cmd - Builds a MSG_CMD_CONFIG_MOTOR configuration frame.
                | build_wait_cmd - Builds a MSG_CMD_WAIT delay pause frame.
                | pack_frame - Serializes a BinaryFrame into raw wire bytes with delimiters.
    '''

    @property
    def name(self) -> str:
        '''
            Gets the builder identifier name.

            :return: Builder name string.
        '''

    def build_frame(self, *, msg_id: MessageId, seq_num: int, payload: bytes = b'') -> BinaryFrame:
        '''
            Constructs and checksums a complete wire protocol BinaryFrame.

            :param msg_id: Command message identifier.
            :param seq_num: Cyclic sequence index (0 - 255).
            :param payload: Raw body bytes (0 to 64 bytes).
            :return: Fully assembled BinaryFrame with valid CRC16.
        '''

    def build_joint_move(self, *, seq_num: int, steps: JointSteps) -> BinaryFrame:
        '''
            Builds a joint step motion frame from JointSteps model.

            :param seq_num: Cyclic sequence index.
            :param steps: JointSteps target instance.
            :return: Assembled BinaryFrame with joint move payload.
        '''

    def build_system_cmd(self, *, msg_id: MessageId, seq_num: int) -> BinaryFrame:
        '''
            Builds a parameterless system command frame (ENABLE, ESTOP, PING, etc.).

            :param msg_id: Target command message identifier.
            :param seq_num: Cyclic sequence index.
            :return: Assembled parameterless BinaryFrame.
        '''

    def build_tool_cmd(self, *, seq_num: int, tool_id: int, state: bool) -> BinaryFrame:
        '''
            Builds a tool actuation command frame (PUMP, VALVE).

            :param seq_num: Cyclic sequence index.
            :param tool_id: Tool identifier (0=PUMP, 1=VALVE).
            :param state: True to activate, False to deactivate.
            :return: Assembled tool command BinaryFrame.
        '''

    def build_motor_config_cmd(
        self, *, seq_num: int, mode: int, axis_mask: int = AxisMask.ALL
    ) -> BinaryFrame:
        '''
            Builds a motor actuation mode configuration frame.

            :param seq_num: Cyclic sequence index.
            :param mode: Motor drive mode integer (0=OPEN_LOOP, 1=CLOSED_LOOP).
            :param axis_mask: Bitmask of target axes (default AxisMask.ALL).
            :return: Assembled motor configuration BinaryFrame.
        '''

    def build_wait_cmd(self, *, delay_ms: int, seq_num: int) -> BinaryFrame:
        '''
            Builds a delay pause command frame (CMD_WAIT).

            :param delay_ms: Dwell duration in milliseconds.
            :param seq_num: Cyclic sequence index.
            :return: Assembled BinaryFrame with packed delay payload.
        '''

    def pack_frame(self, *, frame: BinaryFrame) -> bytes:
        '''
            Encodes the frame into a byte string according to wire format.

            :param frame: BinaryFrame instance.
            :return: Formatted bytes: SOF1 + SOF2 + MSG + SEQ + LEN + DATA + CRC + EOF.
        '''
