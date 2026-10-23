# -*- coding: UTF-8 -*-

'''
Module
    motion.py
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
    Dedicated deserializer decoding motion payloads into JointSteps domain model.
'''

from __future__ import annotations

from struct import unpack
from typing import ClassVar

from scaralang.core.model.exceptions.protocol import ScaraProtocolError
from scaralang.core.model.protocol.payload_size import BinaryPayloadSize
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.infrastructure.protocol.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryMotionPayloadUnpacker:
    '''
        Deserializer decoding raw joint steps binary payloads into JointSteps model.

        It defines:

            :attributes:
                | JOINT_STEPS_FORMAT - Struct format for 22-byte joint step payload.
            :methods:
                | unpack_joint_steps - Deserializes 22-byte joint steps into JointSteps.
                | get_version - Returns component version string.
    '''

    JOINT_STEPS_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOINT_STEPS)

    def unpack_joint_steps(self, data: bytes) -> JointSteps:
        '''
            Deserializes a 22-byte binary payload into a JointSteps instance.

            :param data: Input raw binary bytes.
            :return: JointSteps instance.
            :exceptions: ScaraProtocolError if data is less than 22 bytes.
        '''
        if len(data) < BinaryPayloadSize.JOINT_STEPS:
            raise ScaraProtocolError(
                f'JOINT_STEPS payload too short: expected at least '
                f'{int(BinaryPayloadSize.JOINT_STEPS)} bytes, got {len(data)}'
            )

        values: tuple[int, int, int, int, int, int] = unpack(
            self.JOINT_STEPS_FORMAT, data[:BinaryPayloadSize.JOINT_STEPS]
        )

        return JointSteps(
            target_j1_steps=values[0],
            target_j2_steps=values[1],
            target_z_steps=values[2],
            target_j4_steps=values[3],
            duration_us=values[4],
            feedrate_scale=values[5],
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
