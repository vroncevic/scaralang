# -*- coding: UTF-8 -*-

'''
Module
    toolchain_info_provider_test.py
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
    Unit tests for ToolchainInfoProvider class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.info.toolchain_info_provider import ToolchainInfoProvider

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolchainInfoProvider(TestCase):
    '''
        Test cases verifying ToolchainInfoProvider operations.

        It defines:

            :methods:
                | test_get_toolchain_info_concise - Verifies default concise info output.
                | test_get_toolchain_info_verbose - Verifies verbose info output with bounds.
                | test_get_supported_instructions - Verifies instruction summaries list.
    '''

    def test_get_toolchain_info_concise(self) -> None:
        '''
            Verifies get_toolchain_info returns core specification lines.
        '''
        provider = ToolchainInfoProvider()
        info = provider.get_toolchain_info(verbose=False)
        self.assertIsInstance(info, tuple)
        self.assertTrue(any('scaralang: SCARA' in line for line in info))
        self.assertTrue(any('Version: 1.0.3' in line for line in info))
        self.assertTrue(any('Supported Instructions:' in line for line in info))
        self.assertTrue(any('Binary Protocol Specification:' in line for line in info))
        self.assertFalse(any('Default Kinematic Bounds:' in line for line in info))

    def test_get_toolchain_info_verbose(self) -> None:
        '''
            Verifies get_toolchain_info with verbose=True includes kinematic bounds.
        '''
        provider = ToolchainInfoProvider()
        info = provider.get_toolchain_info(verbose=True)
        self.assertIsInstance(info, tuple)
        self.assertTrue(any('Default Kinematic Bounds:' in line for line in info))
        self.assertTrue(any('L1 = 150.0 mm' in line for line in info))

    def test_get_supported_instructions(self) -> None:
        '''
            Verifies get_supported_instructions returns expected instruction signatures.
        '''
        provider = ToolchainInfoProvider()
        instructions = provider.get_supported_instructions()
        self.assertIsInstance(instructions, tuple)
        self.assertTrue(len(instructions) >= 7)
        self.assertTrue(any('MOVE' in inst for inst in instructions))
        self.assertTrue(any('JUMP' in inst for inst in instructions))
        self.assertTrue(any('ARC' in inst for inst in instructions))
        self.assertTrue(any('WAIT' in inst for inst in instructions))
        self.assertTrue(any('PUMP' in inst for inst in instructions))
        self.assertTrue(any('VALVE' in inst for inst in instructions))
        self.assertTrue(any('HOME' in inst for inst in instructions))

    def test_build_verbose_lines(self) -> None:
        '''
            Verifies build_verbose_lines returns formatted bounds and transmission lines.
        '''
        provider = ToolchainInfoProvider()
        verbose_lines = provider.build_verbose_lines()
        self.assertIsInstance(verbose_lines, tuple)
        self.assertTrue(any('Default Kinematic Bounds:' in line for line in verbose_lines))
        self.assertTrue(any('Default Transmission Parameters:' in line for line in verbose_lines))


if __name__ == '__main__':
    main()
