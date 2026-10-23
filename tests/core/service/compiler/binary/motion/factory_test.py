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
    Unit tests for MotionFactory class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.compiler.binary.motion.dependencies import MotionDependencies
from scaralang.core.service.compiler.binary.motion.factory import MotionFactory
from scaralang.core.service.compiler.binary.motion.icompiler import IMotionCompiler
from scaralang.core.service.compiler.binary.motion.provides import MotionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestMotionFactory(TestCase):
    '''
        Test cases verifying MotionFactory.

        It defines:

            :methods:
                | test_create - Verifies factory returns MotionProvides with IMotionCompiler.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory returns MotionProvides instance with compiler.'''
        mock_discretizer = MagicMock()
        mock_frame_builder = MagicMock()
        mock_frame_packer = MagicMock()
        deps = MotionDependencies(
            discretizer=mock_discretizer,
            frame_builder=mock_frame_builder,
            frame_packer=mock_frame_packer,
        )
        provides = MotionFactory.create(dependencies=deps)
        self.assertIsInstance(provides, MotionProvides)
        self.assertIsInstance(provides.compiler, IMotionCompiler)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(MotionFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
