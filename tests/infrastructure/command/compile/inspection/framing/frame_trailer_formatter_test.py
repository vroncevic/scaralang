# -*- coding: UTF-8 -*-

'''
Module
    frame_trailer_formatter_test.py
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
    Unit tests for FrameTrailerFormatter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.frame_trailer_formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.iframe_trailer_formatter import IFrameTrailerFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameTrailerFormatter(TestCase):
    '''Test suite verifying FrameTrailerFormatter formatting operations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        formatter: FrameTrailerFormatter = FrameTrailerFormatter()
        self.assertTrue(isinstance(formatter, IFrameTrailerFormatter))

    def test_format_trailer(self) -> None:
        '''Verifies formatting frame trailer fields.'''
        formatter: FrameTrailerFormatter = FrameTrailerFormatter()
        result: str = formatter.format_trailer(crc16=0x4B21)
        self.assertEqual(result, '  - Wire Trailer:  CRC16=0x4B21 | EOF=[0D]')


if __name__ == '__main__':
    main()
