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
    Unit tests for PlanProvides dataclass bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.plan.provides import PlanProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanProvides(TestCase):
    '''
        Test cases verifying PlanProvides dataclass.

        It defines:

            :methods:
                | test_attributes - Verifies attributes storage and retrieval.
                | test_immutability - Verifies frozen dataclass immutability.
    '''

    def test_attributes(self) -> None:
        '''
            Verifies attributes are properly stored and accessible.
        '''
        mock_ast_compiler = MagicMock()
        mock_script_compiler = MagicMock()
        provides = PlanProvides(
            ast_compiler=mock_ast_compiler,
            script_compiler=mock_script_compiler,
        )
        self.assertEqual(provides.ast_compiler, mock_ast_compiler)
        self.assertEqual(provides.script_compiler, mock_script_compiler)

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass raises error when mutated.
        '''
        provides = PlanProvides(
            ast_compiler=MagicMock(),
            script_compiler=MagicMock(),
        )
        with self.assertRaises(AttributeError):
            provides.ast_compiler = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
