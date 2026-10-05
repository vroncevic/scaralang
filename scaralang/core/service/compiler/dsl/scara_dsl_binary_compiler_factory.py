# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_binary_compiler_factory.py
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
    Factory instantiating ScaraDslBinaryCompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.ibinary_compiler import IBinaryCompiler
from scaralang.core.service.compiler.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.compiler.dsl.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler import ScaraDslBinaryCompiler
from scaralang.core.service.compiler.scara_compiler_factory import ScaraCompilerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDslBinaryCompilerFactory:
    '''
        Factory providing ScaraDslBinaryCompiler service instances.

        It defines:

            :methods:
                | create - Instantiates ScaraDslBinaryCompiler with injected delegates.
                | create_default - Instantiates ScaraDslBinaryCompiler with standard defaults.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        compiler: IScaraDslCompiler,
        binary_compiler: IBinaryCompiler,
    ) -> IScaraDslBinaryCompiler:
        '''
            Instantiates a configured ScaraDslBinaryCompiler service.

            :param compiler: Required IScaraDslCompiler protocol instance.
            :param binary_compiler: Required IBinaryCompiler protocol instance.
            :return: Fully configured IScaraDslBinaryCompiler protocol instance.
            :exceptions: None.
        '''
        return ScaraDslBinaryCompiler(
            compiler=compiler,
            binary_compiler=binary_compiler,
        )

    @classmethod
    def create_default(cls) -> IScaraDslBinaryCompiler:
        '''
            Builds and returns an IScaraDslBinaryCompiler with standard defaults.

            :return: Fully configured IScaraDslBinaryCompiler protocol instance.
            :exceptions: None.
        '''
        return ScaraCompilerFactory.create_default()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
