# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for SplitterProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.splitter.isplitter import ITokenLineSplitter
from scaralang.core.service.parser.splitter.provides import SplitterProvides
from scaralang.core.service.parser.splitter.splitter import TokenLineSplitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSplitterProvides(TestCase):
    '''
        Test cases verifying SplitterProvides dataclass encapsulation.

        It defines:

            :methods:
                | test_provides_encapsulation - Verifies SplitterProvides stores ITokenLineSplitter.
    '''

    def test_provides_encapsulation(self) -> None:
        '''
            Verifies that SplitterProvides encapsulates ITokenLineSplitter properly.
        '''
        splitter = TokenLineSplitter()
        provides = SplitterProvides(splitter=splitter)
        self.assertIs(provides.splitter, splitter)
        self.assertIsInstance(provides.splitter, ITokenLineSplitter)


if __name__ == '__main__':
    main()
