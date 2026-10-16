# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory for instantiating MotionCommandCompiler coordinators
    with explicit sub-factory dependency injection.
'''

from __future__ import annotations

from scaralang.core.service.compiler.primitive.icompiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.motion.arc.factory import ArcMoveCompilerFactory
from scaralang.core.service.compiler.primitive.motion.cartesian.factory import CartesianMoveCompilerFactory
from scaralang.core.service.compiler.primitive.motion.compiler import MotionCommandCompiler
from scaralang.core.service.compiler.primitive.motion.vertical.factory import VerticalMoveCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandCompilerFactory:
    '''
        Factory providing creation of MotionCommandCompiler coordinator instances.

        It defines:

            :methods:
                | create - Instantiates MotionCommandCompiler delegating to sub-factories.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IPrimitiveCompiler:
        '''
            Creates MotionCommandCompiler with default sub-compilers.

            :return: Fully wired IPrimitiveCompiler instance.
            :exceptions: None.
        '''
        return MotionCommandCompiler(
            sub_compilers=(
                CartesianMoveCompilerFactory.create(),
                VerticalMoveCompilerFactory.create(),
                ArcMoveCompilerFactory.create(),
            )
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
