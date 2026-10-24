# -*- coding: UTF-8 -*-

'''
Module
    iactuator_unpacker.py
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
    Defines IBinaryActuatorPayloadUnpacker protocol for tool and motor payload deserialization.
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
class IBinaryActuatorPayloadUnpacker(Protocol):
    '''
        Structural protocol defining actuator binary payload deserialization contracts.

        It defines:

            :methods:
                | unpack_tool_cmd - Deserializes 2-byte tool command into (tool_id, state).
                | unpack_motor_config - Deserializes 2-byte motor config into (mode, axis_mask).
                | get_version - Returns actuator payload unpacker version string.
    '''

    def unpack_tool_cmd(self, data: bytes) -> tuple[int, bool]:
        '''
            Deserializes a 2-byte binary payload into tool ID and boolean state.

            :param data: Input raw binary bytes.
            :return: Tuple containing (tool_id, state).
        '''

    def unpack_motor_config(self, data: bytes) -> tuple[int, int]:
        '''
            Deserializes a binary payload into motor drive mode and axis mask.

            :param data: Input raw binary bytes.
            :return: Tuple containing (mode, axis_mask).
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
