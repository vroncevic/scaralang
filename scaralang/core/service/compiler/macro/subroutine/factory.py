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
    Factory instantiating and wiring subroutine macro expander subsystem.
'''

from __future__ import annotations

from scaralang.core.service.compiler.macro.segmenter.factory import SegmenterFactory
from scaralang.core.service.compiler.macro.subroutine.dependencies import SubroutineDependencies
from scaralang.core.service.compiler.macro.subroutine.expander import SubroutineExpander
from scaralang.core.service.compiler.macro.subroutine.provides import SubroutineProvides
from scaralang.core.service.compiler.macro.subroutine.registry import SubroutineRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineFactory:
    '''
        Subsystem factory assembling and providing subroutine macro expander services.

        It defines:

            :methods:
                | create - Constructs and wires SubroutineProvides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: SubroutineDependencies | None = None,
    ) -> SubroutineProvides:
        '''
            Constructs and wires SubroutineProvides container.

            :param dependencies: Optional injected SubroutineDependencies bundle.
            :return: Fully configured SubroutineProvides container.
            :exceptions: None.
        '''
        if dependencies is None:
            registry = SubroutineRegistry()
            segmenter = SegmenterFactory.create().segmenter
        else:
            registry = dependencies.registry
            segmenter = dependencies.segmenter

        expander = SubroutineExpander(
            registry=registry,
            segmenter=segmenter,
        )

        return SubroutineProvides(
            expander=expander,
            registry=registry,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
