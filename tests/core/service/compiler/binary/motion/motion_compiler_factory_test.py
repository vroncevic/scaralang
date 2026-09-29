# -*- coding: UTF-8 -*-

'''
Module
    motion_compiler_factory_test.py
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
    Unit tests for MotionCompilerFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.motion.imotion_compiler import IMotionCompiler
from scaralang.core.service.compiler.binary.motion.motion_compiler_factory import MotionCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionCompilerFactory(TestCase):
    '''
        Test cases verifying MotionCompilerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns IMotionCompiler.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory returns IMotionCompiler instance.
        '''
        mock_discretizer = MagicMock()
        mock_frame_builder = MagicMock()
        compiler = MotionCompilerFactory.create(
            discretizer=mock_discretizer,
            frame_builder=mock_frame_builder,
        )
        self.assertIsInstance(compiler, IMotionCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version returns valid string.
        '''
        self.assertEqual(MotionCompilerFactory.get_version(), '1.0.0')


if __name__ == '__main__':
    main()
