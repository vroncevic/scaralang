# -*- coding: UTF-8 -*-

'''
Module
    binary_compiler_factory_test.py
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
    Unit tests for BinaryCompilerFactory class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.binary_compiler_factory import BinaryCompilerFactory
from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryCompilerFactory(TestCase):
    '''
        Test cases verifying BinaryCompilerFactory.

        It defines:

            :methods:
                | test_create_with_collaborators - Verifies factory creation with collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies factory returns IBinaryCompiler instance.
        '''
        mock_disp = MagicMock()
        mock_calc = MagicMock()
        compiler = BinaryCompilerFactory.create(
            step_dispatcher=mock_disp,
            metrics_calculator=mock_calc,
        )
        self.assertIsInstance(compiler, IBinaryCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        self.assertEqual(BinaryCompilerFactory.get_version(), '1.0.0')


if __name__ == '__main__':
    main()
