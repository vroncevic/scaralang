# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for TrailerFactory operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.trailer.factory import TrailerFactory
from scaralang.infrastructure.command.compile.inspection.framing.trailer.formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.iformatter import IFrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.provides import TrailerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrailerFactory(TestCase):
    '''
        Test cases verifying TrailerFactory operations.

        It defines:

            :methods:
                | test_create_returns_provides - Verifies create returns TrailerProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_provides(self) -> None:
        '''
            Verifies factory creates TrailerProvides containing IFrameTrailerFormatter.
        '''
        provides = TrailerFactory.create()
        self.assertIsInstance(provides, TrailerProvides)
        self.assertIsInstance(provides.formatter, IFrameTrailerFormatter)
        self.assertIsInstance(provides.formatter, FrameTrailerFormatter)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(TrailerFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
