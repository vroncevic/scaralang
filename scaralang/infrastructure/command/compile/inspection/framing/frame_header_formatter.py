# -*- coding: UTF-8 -*-

'''
Module
    frame_header_formatter.py
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
    Defines FrameHeaderFormatter formatting wire protocol frame header parameters.
'''

from __future__ import annotations

from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameHeaderFormatter:
    '''
        Formats wire frame header fields into human-readable description.

        It defines:

            :methods:
                | format_header - Formats header delimiters, message, sequence, and length.
                | get_version - Returns the component version string.
    '''

    def format_header(
        self,
        *,
        msg_id: MessageId,
        seq_num: int,
        payload_len: int
    ) -> str:
        '''
            Formats wire frame header fields into human-readable description.

            :param msg_id: Wire frame message identifier.
            :param seq_num: Cyclic frame sequence number.
            :param payload_len: Length of payload in bytes.
            :return: Formatted wire header string.
        '''
        msg_val: int = int(msg_id)
        msg_name: str = msg_id.name

        return (
            f'SOF=[AA 55] | MSG=0x{msg_val:02X} ({msg_name}) | '
            f'SEQ={seq_num:03d} | LEN={payload_len:02d} B'
        )

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: The version string.
        '''
        return __version__
