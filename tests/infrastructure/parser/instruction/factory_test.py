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
    Unit tests for DefaultInstructionParserFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.parser.instruction.iparser import IInstructionLineParser
from scaralang.core.service.parser.instruction.provides import InstructionProvides
from scaralang.infrastructure.parser.instruction.factory import DefaultInstructionParserFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultInstructionParserFactory(TestCase):
    '''
        Test cases verifying DefaultInstructionParserFactory instance creation.

        It defines:

            :methods:
                | test_create - Verifies factory returns default configured InstructionProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies that factory returns default configured InstructionProvides instance.

            :exceptions: None.
        '''
        provides = DefaultInstructionParserFactory.create()
        self.assertIsInstance(provides, InstructionProvides)
        self.assertIsInstance(provides.parser, IInstructionLineParser)
        self.assertEqual(len(provides.parser.handlers), 37)

    def test_get_version(self) -> None:
        '''
            Verifies that get_version returns a valid version string.

            :exceptions: None.
        '''
        version = DefaultInstructionParserFactory.get_version()
        self.assertEqual(version, '1.1.0')


if __name__ == '__main__':
    main()
