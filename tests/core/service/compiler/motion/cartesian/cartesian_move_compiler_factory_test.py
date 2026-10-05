# -*- coding: UTF-8 -*-

'''
Module
    cartesian_move_compiler_factory_test.py
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
    Unit tests for CartesianMoveCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.transformation.iframe_transformer import IFrameTransformer
from scaralang.core.service.compiler.macro.tangent_macro_expander import TangentMacroExpander
from scaralang.core.service.compiler.macro.tangent_macro_expander_factory import TangentMacroExpanderFactory
from scaralang.core.service.compiler.motion.cartesian.cartesian_move_compiler_factory import CartesianMoveCompilerFactory
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCartesianMoveCompilerFactory(TestCase):
    '''
        Test cases verifying CartesianMoveCompilerFactory functionality.

        It defines:

            :methods:
                | test_create - Verifies factory returns configured IMotionSubCompiler.
                | test_create_with_tangent_helper - Verifies factory creation with helper.
                | test_create_with_collaborators - Verifies creation with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create instantiates IMotionSubCompiler instance.
        '''
        compiler = CartesianMoveCompilerFactory.create()
        self.assertIsInstance(compiler, IMotionSubCompiler)

    def test_create_with_tangent_helper(self) -> None:
        '''
            Verifies create_with_tangent_helper returns configured compiler.
        '''
        helper = TangentMacroExpanderFactory.create()
        compiler = CartesianMoveCompilerFactory.create_with_tangent_helper(
            tangent_helper=helper
        )
        self.assertIsInstance(compiler, IMotionSubCompiler)

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies create_with_collaborators instantiates compiler with all dependencies.
        '''
        mock_helper = MagicMock(spec=TangentMacroExpander)
        mock_transformer = MagicMock(spec=IFrameTransformer)
        compiler = CartesianMoveCompilerFactory.create_with_collaborators(
            tangent_helper=mock_helper,
            frame_transformer=mock_transformer,
        )
        self.assertIsInstance(compiler, IMotionSubCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version = CartesianMoveCompilerFactory.get_version()
        self.assertTrue(bool(version))


if __name__ == '__main__':
    main()
