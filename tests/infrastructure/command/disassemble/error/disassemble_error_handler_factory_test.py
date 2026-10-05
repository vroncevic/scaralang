# -*- coding: UTF-8 -*-

'''
Module
    disassemble_error_handler_factory_test.py
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
    Unit tests for DisassembleErrorHandlerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.disassemble.error.disassemble_error_handler import DisassembleErrorHandler
from scaralang.infrastructure.command.disassemble.error.disassemble_error_handler_factory import DisassembleErrorHandlerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDisassembleErrorHandlerFactory(TestCase):
    '''Test cases verifying DisassembleErrorHandlerFactory instantiation and versioning.'''

    def test_create(self) -> None:
        '''Verifies factory creates DisassembleErrorHandler instance.'''
        handler = DisassembleErrorHandlerFactory.create()
        self.assertIsInstance(handler, DisassembleErrorHandler)

    def test_create_default(self) -> None:
        '''Verifies factory creates default DisassembleErrorHandler instance.'''
        handler = DisassembleErrorHandlerFactory.create_default()
        self.assertIsInstance(handler, DisassembleErrorHandler)

    def test_get_version(self) -> None:
        '''Verifies factory version string retrieval.'''
        self.assertEqual(DisassembleErrorHandlerFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
