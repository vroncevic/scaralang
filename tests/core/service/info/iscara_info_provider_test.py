# -*- coding: UTF-8 -*-

'''
Module
    iscara_info_provider_test.py
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
    Unit tests for IScaraInfoProvider interface.
'''

from __future__ import annotations

from typing import Protocol
from unittest import TestCase
from unittest import main

from scaralang.core.service.info.iscara_info_provider import IScaraInfoProvider
from scaralang.core.service.info.scara_info_provider import ScaraInfoProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyInfoProvider:
    '''Dummy info provider satisfying IScaraInfoProvider protocol.'''

    def get_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''Dummy get_info implementation.'''
        _ = verbose
        return ('info',)

    def get_toolchain_info(self, *, verbose: bool = False) -> tuple[str, ...]:
        '''Dummy get_toolchain_info implementation.'''
        _ = verbose
        return ('toolchain_info',)

    def get_supported_instructions(self) -> tuple[str, ...]:
        '''Dummy get_supported_instructions implementation.'''
        return ('MOVE',)

    def build_verbose_lines(self) -> tuple[str, ...]:
        '''Dummy build_verbose_lines implementation.'''
        return ('verbose',)

    def get_version(self) -> str:
        '''Dummy get_version implementation.'''
        return '1.0.4'


class TestIScaraInfoProvider(TestCase):
    '''
        Test cases verifying IScaraInfoProvider interface contract.

        It defines:

            :methods:
                | test_protocol_definition - Verifies protocol methods and runtime checkability.
                | test_scara_info_provider_structural_typing - Verifies ScaraInfoProvider satisfies protocol.
    '''

    def test_protocol_definition(self) -> None:
        '''
            Verifies protocol definition and dummy satisfaction.
        '''
        self.assertTrue(issubclass(IScaraInfoProvider, Protocol))
        self.assertIsInstance(DummyInfoProvider(), IScaraInfoProvider)

    def test_scara_info_provider_structural_typing(self) -> None:
        '''
            Verifies ScaraInfoProvider structurally implements IScaraInfoProvider.
        '''
        provider = ScaraInfoProvider()
        self.assertIsInstance(provider, IScaraInfoProvider)


if __name__ == '__main__':
    main()
