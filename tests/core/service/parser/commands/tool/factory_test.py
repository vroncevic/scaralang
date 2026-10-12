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
    Unit tests for ToolFactory service component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.parser.commands.icommand_parser import ICommandParser
from scaralang.core.service.parser.commands.tool.factory import ToolFactory
from scaralang.core.service.parser.commands.tool.provides import ToolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolFactory(TestCase):
    '''
        Tests for ToolFactory parser instantiation and provides container creation.

        It defines:

            :methods:
                | test_create - Verifies all tool command parsers are instantiated in ToolProvides.
                | test_get_version - Verifies factory version reporting.
    '''

    def test_create(self) -> None:
        '''
            Verifies all 3 tool command parsers are instantiated in ToolProvides container.
        '''
        provides = ToolFactory.create()
        self.assertIsInstance(provides, ToolProvides)
        self.assertEqual(len(provides.parsers), 3)
        for parser in provides.parsers:
            self.assertIsInstance(parser, ICommandParser)

    def test_get_version(self) -> None:
        '''
            Verifies factory version reporting.
        '''
        self.assertEqual(ToolFactory.get_version(), '1.0.8')


if __name__ == '__main__':
    main()
