# -*- coding: UTF-8 -*-

'''
Module
    cartesian_move_compiler_factory.py
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
    Factory for instantiating CartesianMoveCompiler components with dependency injection.
'''

from __future__ import annotations

from scaralang.core.service.compiler.frame.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.compiler.frame.iframe_transformer import IFrameTransformer
from scaralang.core.service.compiler.macro.tangent_macro_expander import TangentMacroExpander
from scaralang.core.service.compiler.macro.tangent_macro_expander_factory import TangentMacroExpanderFactory
from scaralang.core.service.compiler.motion.cartesian.cartesian_move_compiler import CartesianMoveCompiler
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CartesianMoveCompilerFactory:
    '''
        Factory providing creation of CartesianMoveCompiler instances.

        It defines:

            :methods:
                | create - Instantiates CartesianMoveCompiler with wired collaborator factories.
                | create_with_tangent_helper - Instantiates with injected tangent helper.
                | create_with_collaborators - Instantiates with all injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IMotionSubCompiler:
        '''
            Creates CartesianMoveCompiler instance with wired collaborator factories.

            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return CartesianMoveCompiler(
            tangent_helper=TangentMacroExpanderFactory.create(),
            frame_transformer=FrameTransformerFactory.create(),
        )

    @classmethod
    def create_with_tangent_helper(
        cls,
        *,
        tangent_helper: TangentMacroExpander,
    ) -> IMotionSubCompiler:
        '''
            Creates CartesianMoveCompiler instance with injected tangent helper.

            :param tangent_helper: Injected TangentMacroExpander instance.
            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return CartesianMoveCompiler(
            tangent_helper=tangent_helper,
            frame_transformer=FrameTransformerFactory.create(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        tangent_helper: TangentMacroExpander,
        frame_transformer: IFrameTransformer,
    ) -> IMotionSubCompiler:
        '''
            Creates CartesianMoveCompiler instance with all injected collaborators.

            :param tangent_helper: Injected TangentMacroExpander instance.
            :param frame_transformer: Injected IFrameTransformer instance.
            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return CartesianMoveCompiler(
            tangent_helper=tangent_helper,
            frame_transformer=frame_transformer,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
