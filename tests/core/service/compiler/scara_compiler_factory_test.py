# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_factory_test.py
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
    Unit tests for ScaraCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.dsl.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraCompilerFactory(TestCase):
    '''
        Test cases verifying ScaraCompilerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IScaraCompiler with injected delegates.
                | test_create_default - Verifies default factory construction.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory produces IScaraCompiler instance with collaborators.
        '''
        mock_dsl_compiler = MagicMock(spec=IScaraDslCompiler)
        mock_binary_compiler = MagicMock(spec=IBinaryCompiler)
        compiler: IScaraCompiler = ScaraCompilerFactory.create(
            compiler=mock_dsl_compiler,
            binary_compiler=mock_binary_compiler,
        )
        self.assertIsInstance(compiler, IScaraCompiler)

    def test_create_default(self) -> None:
        '''
            Verifies factory produces default IScaraCompiler instance.
        '''
        compiler: IScaraCompiler = ScaraCompilerFactory.create_default()
        self.assertIsInstance(compiler, IScaraCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = ScaraCompilerFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
