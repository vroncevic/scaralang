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
    Factory coordinating assembly of compiler macro subsystem.
'''

from __future__ import annotations

from scaralang.core.service.compiler.macro.dependencies import MacroDependencies
from scaralang.core.service.compiler.macro.frame.factory import FrameMacroExpanderFactory
from scaralang.core.service.compiler.macro.iexpander import IMacroExpander
from scaralang.core.service.compiler.macro.jump.factory import JumpMacroExpanderFactory
from scaralang.core.service.compiler.macro.pallet.dependencies import PalletDependencies
from scaralang.core.service.compiler.macro.pallet.factory import PalletMacroExpanderFactory
from scaralang.core.service.compiler.macro.provides import MacroProvides
from scaralang.core.service.compiler.macro.tangent.factory import TangentMacroExpanderFactory
from scaralang.core.service.compiler.macro.zone.factory import ZoneMacroExpanderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MacroFactory:
    '''
        Factory coordinating creation and wiring of all macro expanders.

        It defines:

            :methods:
                | create - Instantiates and packages all macro expanders.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dependencies: MacroDependencies,
    ) -> MacroProvides:
        '''
            Builds and packages all domain macro expanders.

            :param dependencies: Injected MacroDependencies bundle.
            :return: MacroProvides containing all expanders.
            :exceptions: None.
        '''
        jump_expander: IMacroExpander = JumpMacroExpanderFactory.create()
        frame_expander: IMacroExpander = FrameMacroExpanderFactory.create()
        pallet_expander: IMacroExpander = PalletMacroExpanderFactory.create(
            dependencies=PalletDependencies(
                frame_transformer=dependencies.frame_transformer
            )
        )
        tangent_expander: IMacroExpander = (
            TangentMacroExpanderFactory.create()
        )
        zone_expander: IMacroExpander = (
            ZoneMacroExpanderFactory.create()
        )

        all_expanders: tuple[IMacroExpander, ...] = (
            jump_expander,
            frame_expander,
            pallet_expander,
            tangent_expander,
            zone_expander,
        )

        return MacroProvides(
            expanders=all_expanders,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
