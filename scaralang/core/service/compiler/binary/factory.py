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
    Factory providing composite composition for Binary compiler subsystem using pure DI.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.compiler import BinaryCompiler
from scaralang.core.service.compiler.binary.dependencies import BinaryDependencies
from scaralang.core.service.compiler.binary.provides import BinaryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryFactory:
    '''
        Factory providing composite composition for Binary compiler subsystem using pure DI.

        It defines:

            :methods:
                | create - Wires injected components into a BinaryProvides bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: BinaryDependencies,
    ) -> BinaryProvides:
        '''
            Builds and wires BinaryCompiler with injected dependencies bundle.

            :param dependencies: Injected BinaryDependencies parameter bundle.
            :return: BinaryProvides output bundle exposing IBinaryCompiler.
            :exceptions: None.
        '''
        compiler = BinaryCompiler(dependencies=dependencies)
        return BinaryProvides(compiler=compiler)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
