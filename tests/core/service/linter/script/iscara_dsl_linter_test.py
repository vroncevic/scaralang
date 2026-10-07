# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_linter_test.py
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
    Unit tests for IScaraDslLinter interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.linter.script.iscara_dsl_linter import IScaraDslLinter
from scaralang.core.service.linter.script.scara_script_validator import ScaraScriptValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraDslLinter(TestCase):
    '''
        Test cases verifying IScaraDslLinter interface contract.

        It defines:

            :methods:
                | test_structural_typing - Verifies ScaraScriptValidator satisfies protocol.
                | test_structural_typing_mock - Verifies mock implementation satisfies protocol.
                | test_incompatible_type - Verifies incompatible object does not satisfy protocol.
    '''

    def test_structural_typing(self) -> None:
        '''
            Verifies ScaraScriptValidator structurally implements IScaraDslLinter.
        '''
        validator = ScaraScriptValidator(
            parser=MagicMock(),
            compiler=MagicMock(),
            linter=MagicMock(),
        )
        self.assertIsInstance(validator, IScaraDslLinter)

    def test_structural_typing_mock(self) -> None:
        '''
            Verifies custom mock implementation satisfies IScaraDslLinter.
        '''
        class MockLinter:
            '''Mock linter implementing IScaraDslLinter contract.'''

            def lint_script(self, *, source: str) -> tuple:
                '''Dummy lint_script returning empty tuple.'''
                _ = source
                return ()

            def get_version(self) -> str:
                '''Returns version string.'''
                return '1.0.7'

        self.assertIsInstance(MockLinter(), IScaraDslLinter)

    def test_incompatible_type(self) -> None:
        '''
            Verifies non-conforming object does not satisfy IScaraDslLinter.
        '''
        self.assertFalse(isinstance(object(), IScaraDslLinter))


if __name__ == '__main__':
    main()
