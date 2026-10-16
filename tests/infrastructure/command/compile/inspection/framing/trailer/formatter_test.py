# -*- coding: UTF-8 -*-

'''
Module
    formatter_test.py
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
    Unit tests for FrameTrailerFormatter.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.trailer.formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.iformatter import IFrameTrailerFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameTrailerFormatter(TestCase):
    '''Test cases verifying FrameTrailerFormatter formatting functionality.'''

    def setUp(self) -> None:
        '''Initializes formatter instance.'''
        self.formatter = FrameTrailerFormatter()

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertIsInstance(self.formatter, IFrameTrailerFormatter)

    def test_get_version(self) -> None:
        '''Verifies component version string retrieval.'''
        self.assertEqual(self.formatter.get_version(), '1.0.9')

    def test_format_trailer(self) -> None:
        '''Verifies formatting of wire trailer line.'''
        line: str = self.formatter.format_trailer(crc16=0x1234)
        self.assertIn('CRC16=0x1234', line)
        self.assertIn('EOF=[0D]', line)


if __name__ == '__main__':
    main()
