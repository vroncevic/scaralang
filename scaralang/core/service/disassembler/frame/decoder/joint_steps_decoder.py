# -*- coding: UTF-8 -*-

'''
Module
    joint_steps_decoder.py
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
    Decoder for joint step displacement binary frame payloads.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JointStepsDecoder:
    '''
        Decodes joint step displacement payloads into human-readable coordinate strings.

        It defines:

            :attributes:
                | _MSG_ID - Message identifier for joint steps displacement command.
                | _unpacker - Injected motion payload unpacker protocol strategy.
            :methods:
                | __init__ - Initializes decoder with injected unpacker.
                | can_decode - Checks if message ID matches joint steps command.
                | decode - Decodes joint steps payload into formatted detail string.
                | get_version - Returns decoder version string.
    '''

    _MSG_ID: ClassVar[int] = int(MessageId.CMD_MOVE_JOINT_STEPS)

    _unpacker: IBinaryMotionPayloadUnpacker

    def __init__(self, *, unpacker: IBinaryMotionPayloadUnpacker) -> None:
        '''
            Initializes JointStepsDecoder with required payload unpacker.

            :param unpacker: Injected IBinaryMotionPayloadUnpacker protocol strategy.
            :exceptions: None.
        '''
        self._unpacker: Final[IBinaryMotionPayloadUnpacker] = unpacker

    def can_decode(self, *, msg_id: int) -> bool:
        '''
            Evaluates whether this decoder handles joint steps displacement command.

            :param msg_id: Numeric message identifier.
            :return: True if CMD_MOVE_JOINT_STEPS, False otherwise.
            :exceptions: None.
        '''
        return msg_id == self._MSG_ID

    def decode(self, *, frame: BinaryFrame) -> str:
        '''
            Decodes joint step displacement payload into formatted coordinate string.

            :param frame: BinaryFrame instance containing joint steps payload.
            :return: Formatted coordinate string.
            :exceptions: None.
        '''
        steps: JointSteps = self._unpacker.unpack_joint_steps(frame.payload)
        return (
            f'J1={steps.target_j1_steps} J2={steps.target_j2_steps} '
            f'Z={steps.target_z_steps} J4={steps.target_j4_steps} '
            f'dur={steps.duration_us}us'
        )

    def get_version(self) -> str:
        '''
            Returns the decoder version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
