# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for CompileDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.infrastructure.command.compile.dependencies import CompileDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCompileDependencies(TestCase):
    '''
        Test cases verifying CompileDependencies data carrier.

        It defines:

            :methods:
                | test_dependencies_initialization - Verifies valid bundle instantiation.
                | test_dependencies_immutability - Verifies frozen dataclass behavior.
    '''

    def setUp(self) -> None:
        '''Sets up mock dependencies and collaborator bundle.'''
        self.mock_compiler = MagicMock()
        self.mock_inspection_presenter = MagicMock()
        self.mock_telemetry_formatter = MagicMock()
        self.mock_error_handler = MagicMock()
        self.dependencies = CompileDependencies(
            compiler=self.mock_compiler,
            inspection_presenter=self.mock_inspection_presenter,
            telemetry_formatter=self.mock_telemetry_formatter,
            error_handler=self.mock_error_handler,
        )

    def test_dependencies_initialization(self) -> None:
        '''Verifies fields are correctly initialized.'''
        self.assertIs(self.dependencies.compiler, self.mock_compiler)
        self.assertIs(
            self.dependencies.inspection_presenter,
            self.mock_inspection_presenter,
        )
        self.assertIs(
            self.dependencies.telemetry_formatter,
            self.mock_telemetry_formatter,
        )
        self.assertIs(self.dependencies.error_handler, self.mock_error_handler)

    def test_dependencies_immutability(self) -> None:
        '''Verifies bundle is frozen and fields cannot be mutated.'''
        with self.assertRaises(FrozenInstanceError):
            self.dependencies.compiler = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
