# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for MacroFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.macro.dependencies import MacroDependencies
from scaralang.core.service.compiler.macro.factory import MacroFactory
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.provides import MacroProvides
from scaralang.core.service.transformation.itransformer import ITransformer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMacroFactory(TestCase):
    '''
        Test cases verifying MacroFactory behavior.
    '''

    def test_create(self) -> None:
        '''
            Verifies creation and packaging of all macro expanders.
        '''
        mock_transformer = MagicMock(spec=ITransformer)
        deps = MacroDependencies(frame_transformer=mock_transformer)
        provides = MacroFactory.create(dependencies=deps)

        self.assertIsInstance(provides, MacroProvides)
        self.assertEqual(len(provides.expanders), 5)
        for expander in provides.expanders:
            self.assertIsInstance(expander, IMacroExpander)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns string.
        '''
        version = MacroFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
