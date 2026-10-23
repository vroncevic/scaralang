# -*- coding: UTF-8 -*-

'''
Module
    ilinter_test.py
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
    Unit tests for IScriptLinter role interface.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.linter.script.dependencies import ScriptDependencies
from scaralang.core.service.linter.script.ilinter import IScriptLinter
from scaralang.core.service.linter.script.linter import ScriptLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScriptLinter(TestCase):
    '''
        Test cases verifying IScriptLinter role interface contract.

        It defines:

            :methods:
                | test_structural_typing - Verifies ScriptLinter satisfies protocol.
                | test_structural_typing_mock - Verifies mock implementation satisfies protocol.
                | test_incompatible_type - Verifies incompatible object does not satisfy protocol.
    '''

    def test_structural_typing(self) -> None:
        '''
            Verifies ScriptLinter structurally implements IScriptLinter.
        '''
        linter = ScriptLinter(
            dependencies=ScriptDependencies(
                parser=MagicMock(),
                linter=MagicMock(),
            )
        )
        self.assertIsInstance(linter, IScriptLinter)

    def test_structural_typing_mock(self) -> None:
        '''
            Verifies arbitrary mock with matching methods satisfies protocol.
        '''
        mock_linter = MagicMock(spec=IScriptLinter)
        self.assertIsInstance(mock_linter, IScriptLinter)

    def test_incompatible_type(self) -> None:
        '''
            Verifies incompatible object does not satisfy IScriptLinter.
        '''
        self.assertNotIsInstance('not_a_linter', IScriptLinter)


if __name__ == '__main__':
    main()
