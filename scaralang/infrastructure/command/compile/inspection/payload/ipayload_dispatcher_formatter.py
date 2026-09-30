# -*- coding: UTF-8 -*-

'''
Module
    ipayload_dispatcher_formatter.py
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
    Defines structural interface protocol for dispatching frame payload formatting.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.message_id import MessageId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPayloadDispatcherFormatter(Protocol):
    '''
        Structural interface protocol for routing frame payload presentation formatting.

        It defines:

            :methods:
                | format_payload - Dispatches frame payload formatting based on MessageId.
    '''

    def format_payload(self, *, msg_id: MessageId, payload: bytes) -> str:
        '''
            Routes payload formatting to specialized formatters or emits generic hex dump.

            :param msg_id: Message type identifier.
            :param payload: Raw wire payload bytes.
            :return: Formatted presentation string.
        '''
