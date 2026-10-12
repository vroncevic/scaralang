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
    Unit tests for BinaryProvides output bundle.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.icompiler import IBinaryCompiler
from scaralang.core.service.compiler.binary.provides import BinaryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryProvides(TestCase):
    '''
        Test cases verifying BinaryProvides dataclass behavior.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are set correctly.
                | test_immutability - Verifies frozen behavior on attribute modification.
    '''

    def test_initialization(self) -> None:
        '''Verifies attributes are set correctly.'''
        mock_compiler = MagicMock(spec=IBinaryCompiler)
        provides = BinaryProvides(compiler=mock_compiler)
        self.assertIs(provides.compiler, mock_compiler)

    def test_immutability(self) -> None:
        '''Verifies frozen behavior on attribute modification.'''
        mock_compiler = MagicMock(spec=IBinaryCompiler)
        provides = BinaryProvides(compiler=mock_compiler)
        with self.assertRaises(FrozenInstanceError):
            provides.compiler = mock_compiler  # type: ignore[misc]


if __name__ == '__main__':
    main()
