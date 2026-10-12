# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for DecompileProvides dataclass container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.infrastructure.command.decompile.provides import DecompileProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDecompileProvides(TestCase):
    '''
        Test cases verifying DecompileProvides provider container.

        It defines:

            :methods:
                | test_provides_initialization - Verifies valid container instantiation.
                | test_provides_immutability - Verifies frozen dataclass behavior.
    '''

    def setUp(self) -> None:
        '''Sets up mock executor and definition.'''
        self.mock_executor = MagicMock()
        self.mock_definition = MagicMock()
        self.provides = DecompileProvides(
            executor=self.mock_executor,
            definition=self.mock_definition,
        )

    def test_provides_initialization(self) -> None:
        '''Verifies provides container retains all collaborator references.'''
        self.assertIs(self.provides.executor, self.mock_executor)
        self.assertIs(self.provides.definition, self.mock_definition)

    def test_provides_immutability(self) -> None:
        '''Verifies provides container enforces immutability via frozen dataclass.'''
        with self.assertRaises(FrozenInstanceError):
            self.provides.executor = self.mock_executor  # type: ignore[misc]


if __name__ == '__main__':
    main()
