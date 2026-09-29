# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_bundle_test.py
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
    Unit tests for ScaraDslBundle class.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.dsl.scara_dsl_bundle import ScaraDslBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslBundle(TestCase):
    '''
        Test cases verifying ScaraDslBundle dataclass.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle correctly stores injected attributes.
                | test_bundle_immutability - Verifies bundle is frozen against attribute mutation.
    '''

    def test_bundle_attributes(self) -> None:
        '''
            Verifies bundle stores all injected protocol references.
        '''
        mock_compiler = MagicMock()
        mock_validator = MagicMock()
        mock_exporter = MagicMock()
        mock_binary_service = MagicMock()
        mock_toolchain_info = MagicMock()

        bundle = ScaraDslBundle(
            compiler=mock_compiler,
            validator=mock_validator,
            exporter=mock_exporter,
            binary_service=mock_binary_service,
            toolchain_info=mock_toolchain_info,
        )

        self.assertIs(bundle.compiler, mock_compiler)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.exporter, mock_exporter)
        self.assertIs(bundle.binary_service, mock_binary_service)
        self.assertIs(bundle.toolchain_info, mock_toolchain_info)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies bundle fields cannot be modified after instantiation.
        '''
        bundle = ScaraDslBundle(
            compiler=MagicMock(),
            validator=MagicMock(),
            exporter=MagicMock(),
            binary_service=MagicMock(),
            toolchain_info=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.compiler = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
