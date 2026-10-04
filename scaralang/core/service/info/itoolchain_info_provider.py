# -*- coding: UTF-8 -*-

'''
Module
    itoolchain_info_provider.py
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
    Defines interface IToolchainInfoProvider for querying SCARA toolchain metadata.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolchainInfoProvider(Protocol):
    '''
        Protocol defining toolchain metadata and instruction catalog provider contract.

        It defines:

            :methods:
                | get_toolchain_info - Returns formatted toolchain specification lines.
                | get_supported_instructions - Returns list of supported DSL instruction names.
                | build_verbose_lines - Returns detailed kinematic bounds and transmission lines.
    '''

    def get_toolchain_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''
            Returns toolchain metadata, instruction catalog and protocol specification.

            :param verbose: Whether to include kinematic bounds details.
            :return: Tuple of informative strings.
            :exceptions: None.
        '''

    def get_supported_instructions(self) -> tuple[str, ...]:
        '''
            Returns list of supported DSL instruction syntax summaries.

            :return: Tuple of supported instruction names and signatures.
            :exceptions: None.
        '''

    def build_verbose_lines(self) -> tuple[str, ...]:
        '''
            Builds detailed kinematic bounds and transmission lines.

            :return: Tuple of formatted verbose specification lines.
            :exceptions: None.
        '''
