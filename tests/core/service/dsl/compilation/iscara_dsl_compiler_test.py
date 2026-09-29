# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_compiler_test.py
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
    Unit tests for IScaraDslCompiler interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.dsl.compilation.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.dsl.compilation.scara_dsl_compiler import ScaraDslCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraDslCompiler(TestCase):
    '''
        Test cases verifying IScaraDslCompiler interface contract.

        It defines:

            :methods:
                | test_structural_typing - Verifies ScaraDslCompiler satisfies protocol.
    '''

    def test_structural_typing(self) -> None:
        '''
            Verifies ScaraDslCompiler structurally implements IScaraDslCompiler.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        compiler = ScaraDslCompiler(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        self.assertIsInstance(compiler, IScaraDslCompiler)


if __name__ == '__main__':
    main()
