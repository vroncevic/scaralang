# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_binary_compiler_test.py
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
    Unit tests for IScaraDslBinaryCompiler protocol and structural subtyping.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler import ScaraDslBinaryCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraDslBinaryCompiler(TestCase):
    '''
        Test cases verifying IScaraDslBinaryCompiler protocol and structural typing.

        It defines:

            :methods:
                | test_structural_typing_concrete - Verifies ScaraDslBinaryCompiler satisfies protocol.
                | test_structural_typing_mock - Verifies mock implementation satisfies protocol.
                | test_incompatible_type - Verifies non-conforming object fails check.
    '''

    def test_structural_typing_concrete(self) -> None:
        '''
            Verifies ScaraDslBinaryCompiler satisfies IScaraDslBinaryCompiler protocol.
        '''
        compiler = ScaraDslBinaryCompiler(
            compiler=MagicMock(),
            binary_compiler=MagicMock(),
        )
        self.assertIsInstance(compiler, IScaraDslBinaryCompiler)

    def test_structural_typing_mock(self) -> None:
        '''
            Verifies mock implementing binary compiler methods satisfies protocol.
        '''
        mock_compiler = MagicMock()
        mock_compiler.compile_plan = MagicMock()
        mock_compiler.compile_to_binary = MagicMock()
        mock_compiler.compile_to_bytes = MagicMock()
        mock_compiler.get_program_telemetry = MagicMock()
        self.assertIsInstance(mock_compiler, IScaraDslBinaryCompiler)

    def test_incompatible_type(self) -> None:
        '''
            Verifies object missing protocol methods fails type check.
        '''
        self.assertFalse(isinstance(object(), IScaraDslBinaryCompiler))


if __name__ == '__main__':
    main()
