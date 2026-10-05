# -*- coding: UTF-8 -*-

'''
Module
    frame_header_formatter_test.py
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
    Unit tests for FrameHeaderFormatter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.command.compile.inspection.framing.frame_header_formatter import FrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.iframe_header_formatter import IFrameHeaderFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameHeaderFormatter(TestCase):
    '''Test suite verifying FrameHeaderFormatter formatting operations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        formatter: FrameHeaderFormatter = FrameHeaderFormatter()
        self.assertTrue(isinstance(formatter, IFrameHeaderFormatter))
        self.assertFalse(isinstance(object(), IFrameHeaderFormatter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        formatter: FrameHeaderFormatter = FrameHeaderFormatter()
        self.assertEqual(formatter.get_version(), '1.0.5')

    def test_format_header(self) -> None:
        '''Verifies formatting frame header fields.'''
        formatter: FrameHeaderFormatter = FrameHeaderFormatter()
        result: str = formatter.format_header(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload_len=22,
        )
        self.assertIn('SOF=[AA 55]', result)
        self.assertIn('MSG=0x01 (CMD_MOVE_JOINT_STEPS)', result)
        self.assertIn('SEQ=001', result)
        self.assertIn('LEN=22 B', result)


if __name__ == '__main__':
    main()
