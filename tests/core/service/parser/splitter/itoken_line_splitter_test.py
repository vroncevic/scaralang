# -*- coding: UTF-8 -*-

'''
Module
    itoken_line_splitter_test.py
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
    Unit tests for ITokenLineSplitter protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.splitter.itoken_line_splitter import ITokenLineSplitter
from scaralang.core.service.parser.splitter.token_line_splitter import TokenLineSplitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestITokenLineSplitter(TestCase):
    '''
        Test cases verifying ITokenLineSplitter structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies TokenLineSplitter satisfies protocol.
                | test_name_property - Verifies name property returns expected identifier.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that TokenLineSplitter satisfies ITokenLineSplitter.
        '''
        splitter = TokenLineSplitter()
        self.assertIsInstance(splitter, ITokenLineSplitter)

    def test_name_property(self) -> None:
        '''
            Verifies that name property returns expected identifier.
        '''
        splitter = TokenLineSplitter()
        self.assertEqual(splitter.name, 'token_line_splitter')


if __name__ == '__main__':
    main()
