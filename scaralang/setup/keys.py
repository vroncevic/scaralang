# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the scaralang bundle.
'''

from __future__ import annotations

from types import MappingProxyType
from typing import ClassVar

from ats_utilities.base.setup.bundle import BaseBundle

from scaralang.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangBundleKeys:
    '''
        Runtime components and interface constraints for the scaralang bundle.

        It defines:

            :attributes:
                | DEPENDENCY_BASE - Base bundle key.
                | DEPENDENCY_CLI - CLI adapter key.
                | OPTION_INFO_FILE - Info file configuration key.
                | OPTION_VERBOSE - Verbose option key.
            :methods:
                | get_dependency_to_type - Returns mapping of bundle dependencies to types.
                | get_option_to_type - Returns mapping of bundle options to types.
    '''

    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_CLI: ClassVar[str] = 'cli'

    OPTION_INFO_FILE: ClassVar[str] = 'info_file'
    OPTION_VERBOSE: ClassVar[str] = 'verbose'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of bundle dependencies to their expected types.

            :return: MappingProxyType mapping dependency keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_BASE: BaseBundle,
            cls.DEPENDENCY_CLI: ICLI,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of bundle options to their expected types.

            :return: MappingProxyType mapping option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
            cls.OPTION_VERBOSE: bool,
        })
