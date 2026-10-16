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
    Unit tests for ExportDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.infrastructure.command.export.dependencies import ExportDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExportDependencies(TestCase):
    '''
        Test cases verifying ExportDependencies data carrier.

        It defines:

            :methods:
                | test_dependencies_initialization - Verifies valid bundle instantiation.
                | test_dependencies_immutability - Verifies frozen dataclass behavior.
    '''

    def setUp(self) -> None:
        '''Sets up mock dependencies and collaborator bundle.'''
        self.mock_service = MagicMock()
        self.mock_dispatcher = MagicMock()
        self.mock_error_handler = MagicMock()
        self.dependencies = ExportDependencies(
            service=self.mock_service,
            dispatcher=self.mock_dispatcher,
            error_handler=self.mock_error_handler,
        )

    def test_dependencies_initialization(self) -> None:
        '''Verifies dependencies container retains all collaborator references.'''
        self.assertIs(self.dependencies.service, self.mock_service)
        self.assertIs(self.dependencies.dispatcher, self.mock_dispatcher)
        self.assertIs(self.dependencies.error_handler, self.mock_error_handler)

    def test_dependencies_immutability(self) -> None:
        '''Verifies dependencies container enforces immutability via frozen dataclass.'''
        with self.assertRaises(FrozenInstanceError):
            self.dependencies.service = self.mock_service  # type: ignore[misc]


if __name__ == '__main__':
    main()
