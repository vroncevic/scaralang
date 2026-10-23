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
    Unit tests for MacroProvides dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.provides import MacroProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMacroProvides(TestCase):
    '''
        Test cases verifying MacroProvides behavior and immutability.
    '''

    def test_instantiation_and_attributes(self) -> None:
        '''
            Verifies initialization and fields.
        '''
        mock_expander = MagicMock(spec=IMacroExpander)
        provides = MacroProvides(
            expanders=(mock_expander,),
        )
        self.assertEqual(provides.expanders, (mock_expander,))

    def test_immutability(self) -> None:
        '''
            Verifies frozen dataclass immutability.
        '''
        mock_expander = MagicMock(spec=IMacroExpander)
        provides = MacroProvides(
            expanders=(mock_expander,),
        )
        with self.assertRaises(AttributeError):
            provides.expanders = ()  # type: ignore[misc]


if __name__ == '__main__':
    main()
