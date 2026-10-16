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
    Unit tests for VerticalMoveCompilerFactory component.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.primitive.motion.isub_compiler import IMotionSubCompiler
from scaralang.core.service.compiler.primitive.motion.vertical.compiler import VerticalMoveCompiler
from scaralang.core.service.compiler.primitive.motion.vertical.factory import VerticalMoveCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestVerticalMoveCompilerFactory(TestCase):
    '''
        Test cases verifying VerticalMoveCompilerFactory functionality.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates IMotionSubCompiler.
                | test_get_version - Verifies factory returns valid version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns a configured VerticalMoveCompiler instance.
        '''
        compiler = VerticalMoveCompilerFactory.create()
        self.assertIsInstance(compiler, IMotionSubCompiler)
        self.assertIsInstance(compiler, VerticalMoveCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(VerticalMoveCompilerFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
