# -*- coding: UTF-8 -*-

'''
Module
    frame_header_formatter_factory_test.py
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
    Unit tests for FrameHeaderFormatterFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.frame_header_formatter import FrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.frame_header_formatter_factory import FrameHeaderFormatterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameHeaderFormatterFactory(TestCase):
    '''
        Test suite verifying FrameHeaderFormatterFactory instantiation.

        It defines:

            :methods:
                | test_create - Verifies factory creates a FrameHeaderFormatter instance.
                | test_get_version - Verifies factory returns version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory creates a FrameHeaderFormatter instance.'''
        instance = FrameHeaderFormatterFactory.create()
        self.assertIsInstance(instance, FrameHeaderFormatter)

    def test_get_version(self) -> None:
        '''Verifies factory returns a valid semantic version string.'''
        version: str = FrameHeaderFormatterFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
