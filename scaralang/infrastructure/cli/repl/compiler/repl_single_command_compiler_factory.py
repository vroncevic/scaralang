# -*- coding: UTF-8 -*-

'''
Module
    repl_single_command_compiler_factory.py
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
    Factory instantiating ReplSingleCommandCompiler instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.compiler.dsl.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler_factory import ScaraDslBinaryCompilerFactory
from scaralang.core.service.compiler.dsl.scara_dsl_compiler_factory import ScaraDslCompilerFactory
from scaralang.infrastructure.cli.repl.compiler.repl_single_command_compiler import ReplSingleCommandCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplSingleCommandCompilerFactory:
    '''
        Factory providing ReplSingleCommandCompiler instances.

        It defines:

            :methods:
                | create - Builds ReplSingleCommandCompiler instance.
                | create_default - Builds ReplSingleCommandCompiler with default collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        compiler: IScaraDslCompiler,
        binary_compiler: IScaraDslBinaryCompiler,
    ) -> ReplSingleCommandCompiler:
        '''
            Builds and returns a ReplSingleCommandCompiler instance.

            :param compiler: Injected IScaraDslCompiler protocol instance.
            :param binary_compiler: Injected IScaraDslBinaryCompiler protocol instance.
            :return: Instantiated ReplSingleCommandCompiler instance.
            :exceptions: None.
        '''
        return ReplSingleCommandCompiler(
            compiler=compiler,
            binary_compiler=binary_compiler,
        )

    @classmethod
    def create_default(cls) -> ReplSingleCommandCompiler:
        '''
            Builds and returns a ReplSingleCommandCompiler with default collaborators.

            :return: Instantiated ReplSingleCommandCompiler instance.
            :exceptions: None.
        '''
        return ReplSingleCommandCompiler(
            compiler=ScaraDslCompilerFactory.create_default(),
            binary_compiler=ScaraDslBinaryCompilerFactory.create_default(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
