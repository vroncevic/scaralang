# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_assembler_factory_test.py
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
    Unit tests for BinaryFrameAssemblerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_assembler import BinaryFrameAssembler
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_assembler_factory import BinaryFrameAssemblerFactory
from scaralang.infrastructure.communication.protocol.binary.parser.ibinary_frame_assembler import IBinaryFrameAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFrameAssemblerFactory(TestCase):
    '''
        Test suite verifying BinaryFrameAssemblerFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates assembler.
                | test_structural_typing - Verifies instance satisfies IBinaryFrameAssembler.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''Verifies factory creates a valid BinaryFrameAssembler instance.'''
        assembler = BinaryFrameAssemblerFactory.create()
        self.assertIsInstance(assembler, BinaryFrameAssembler)

    def test_structural_typing(self) -> None:
        '''Verifies created instance satisfies IBinaryFrameAssembler protocol.'''
        assembler = BinaryFrameAssemblerFactory.create()
        self.assertIsInstance(assembler, IBinaryFrameAssembler)

    def test_get_version(self) -> None:
        '''Verifies factory returns a valid version string.'''
        version: str = BinaryFrameAssemblerFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
