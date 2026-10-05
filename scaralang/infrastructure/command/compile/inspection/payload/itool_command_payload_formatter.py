# -*- coding: UTF-8 -*-

'''
Module
    itool_command_payload_formatter.py
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
    Defines structural interface protocol for tool command payload presentation formatting.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolCommandPayloadFormatter(Protocol):
    '''
        Structural interface protocol for formatting tool command actuation payloads.

        It defines:

            :methods:
                | format_tool_cmd - Formats tool actuation parameters and raw hex bytes.
                | get_version - Returns the interface protocol version identifier.
    '''

    def format_tool_cmd(
        self,
        *,
        tool_id: int,
        state: bool,
        raw_payload: bytes
    ) -> str:
        '''
            Formats tool ID, state, and raw hex bytes into human-readable representation.

            :param tool_id: Numeric tool identifier (0=PUMP, 1=VALVE).
            :param state: Tool activation state (True=ON, False=OFF).
            :param raw_payload: Raw payload byte sequence.
            :return: Formatted presentation string.
        '''

    def get_version(self) -> str:
        '''
            Returns the interface protocol version identifier.

            :return: The protocol version string.
        '''
