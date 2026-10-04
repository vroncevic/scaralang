# -*- coding: UTF-8 -*-

'''
Module
    tool_command_payload_formatter.py
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
    Defines ToolCommandPayloadFormatter formatting pneumatic tool payloads for inspection.
'''

from __future__ import annotations

from typing import Final

from scaralang.infrastructure.command.compile.inspection.framing.ihex_stream_formatter import IHexStreamFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandPayloadFormatter:
    '''
        Formats pneumatic tool actuation payloads into human-readable multi-line presentation.

        It defines:

            :attributes:
                | _hex_formatter - Injected hex stream formatter strategy.
            :methods:
                | __init__ - Initializes formatter with injected hex stream formatter.
                | format_tool_cmd - Formats tool actuation parameters and raw hex bytes.
                | get_version - Returns the component version string.
    '''

    _hex_formatter: IHexStreamFormatter

    def __init__(self, *, hex_formatter: IHexStreamFormatter) -> None:
        '''
            Initializes ToolCommandPayloadFormatter with injected hex formatter.

            :param hex_formatter: Injected hex stream formatter.
        '''
        self._hex_formatter: Final[IHexStreamFormatter] = hex_formatter

    def format_tool_cmd(
        self,
        *,
        tool_id: int,
        state: bool,
        raw_payload: bytes
    ) -> str:
        '''
            Formats tool ID, state, and raw hex bytes into human-readable presentation.

            :param tool_id: Numeric tool identifier (0=PUMP, 1=VALVE).
            :param state: Tool activation state (True=ON, False=OFF).
            :param raw_payload: Raw payload byte sequence.
            :return: Formatted presentation string.
        '''
        tool_name: str = (
            'PUMP' if tool_id == 0 else ('VALVE' if tool_id == 1 else f'TOOL_{tool_id}')
        )
        state_str: str = 'ACTIVE (1)' if state else 'INACTIVE (0)'
        hex_str: str = self._hex_formatter.format_bytes(data=raw_payload)
        struct_line: str = f'  - Packed Struct: Tool={tool_name} (id={tool_id}) | State={state_str}'
        hex_line: str = f'  - Payload Hex:   {hex_str}'

        return f'{struct_line}\n{hex_line}'

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: The version string.
        '''
        return __version__
