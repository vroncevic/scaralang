# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for ScriptDependencies dataclass bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.plan.script.dependencies import ScriptDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScriptDependencies(TestCase):
    '''
        Test cases verifying ScriptDependencies dataclass.

        It defines:

            :methods:
                | test_attributes - Verifies attributes storage and retrieval.
                | test_immutability - Verifies frozen dataclass immutability.
    '''

    def test_attributes(self) -> None:
        '''
            Verifies attributes are properly stored and accessible.
        '''
        mock_parser = MagicMock()
        mock_compiler = MagicMock()
        mock_linter = MagicMock()
        deps = ScriptDependencies(
            parser=mock_parser,
            compiler=mock_compiler,
            linter=mock_linter,
        )
        self.assertEqual(deps.parser, mock_parser)
        self.assertEqual(deps.compiler, mock_compiler)
        self.assertEqual(deps.linter, mock_linter)

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass raises error when mutated.
        '''
        deps = ScriptDependencies(
            parser=MagicMock(),
            compiler=MagicMock(),
            linter=MagicMock(),
        )
        with self.assertRaises(AttributeError):
            deps.parser = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
