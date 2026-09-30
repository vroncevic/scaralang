# -*- coding: UTF-8 -*-

'''
Module
    tool_command_payload_formatter_test.py
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
    Unit tests for ToolCommandPayloadFormatter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.itool_command_payload_formatter import IToolCommandPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool_command_payload_formatter import ToolCommandPayloadFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolCommandPayloadFormatter(TestCase):
    '''Test suite verifying ToolCommandPayloadFormatter formatting operations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        formatter: ToolCommandPayloadFormatter = ToolCommandPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        self.assertTrue(isinstance(formatter, IToolCommandPayloadFormatter))

    def test_format_tool_cmd_pump(self) -> None:
        '''Verifies formatting of pump tool command.'''
        formatter: ToolCommandPayloadFormatter = ToolCommandPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        result: str = formatter.format_tool_cmd(tool_id=0, state=True, raw_payload=b'\x00\x01')
        self.assertIn('Tool=PUMP (id=0)', result)
        self.assertIn('State=ACTIVE (1)', result)
        self.assertIn('00 01', result)

    def test_format_tool_cmd_valve(self) -> None:
        '''Verifies formatting of valve tool command.'''
        formatter: ToolCommandPayloadFormatter = ToolCommandPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        result: str = formatter.format_tool_cmd(tool_id=1, state=False, raw_payload=b'\x01\x00')
        self.assertIn('Tool=VALVE (id=1)', result)
        self.assertIn('State=INACTIVE (0)', result)


if __name__ == '__main__':
    main()
