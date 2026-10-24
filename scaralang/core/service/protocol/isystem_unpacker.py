# -*- coding: UTF-8 -*-

'''
Module
    isystem_unpacker.py
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
    Defines IBinarySystemPayloadUnpacker protocol for system and jog payload deserialization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinarySystemPayloadUnpacker(Protocol):
    '''
        Structural protocol defining system command payload deserialization contracts.

        It defines:

            :methods:
                | unpack_jog_payload - Deserializes joint jog command payload into (joint_id, step, speed).
                | unpack_override - Deserializes speed override command payload into percentage integer.
                | get_version - Returns system payload unpacker version string.
    '''

    def unpack_jog_payload(self, data: bytes) -> tuple[int, int, int]:
        '''
            Deserializes a joint jog command payload into joint index, step, and speed.

            :param data: Input raw binary bytes.
            :return: Tuple containing (joint_id, step, speed).
        '''

    def unpack_override(self, data: bytes) -> int:
        '''
            Deserializes a speed override command payload into percentage integer.

            :param data: Input raw binary bytes.
            :return: Speed override percentage.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
