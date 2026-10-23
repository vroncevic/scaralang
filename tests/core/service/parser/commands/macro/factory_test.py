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
    Unit tests for MacroFactory service component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.parser.commands.iparser import ICommandParser
from scaralang.core.service.parser.commands.macro.factory import MacroFactory
from scaralang.core.service.parser.commands.macro.provides import MacroProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMacroFactory(TestCase):
    '''
        Tests for MacroFactory parser instantiation and provides container creation.

        It defines:

            :methods:
                | test_create - Verifies all macro command parsers are instantiated in MacroProvides.
                | test_get_version - Verifies factory version reporting.
    '''

    def test_create(self) -> None:
        '''
            Verifies all 7 macro command parsers are instantiated in MacroProvides container.

            :exceptions: None.
        '''
        provides = MacroFactory.create()
        self.assertIsInstance(provides, MacroProvides)
        self.assertEqual(len(provides.parsers), 7)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_get_version(self) -> None:
        '''
            Verifies factory version reporting.

            :exceptions: None.
        '''
        self.assertEqual(MacroFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
