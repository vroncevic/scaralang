# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for ReplCommandBundle dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.infrastructure.command.repl.bundle import ReplCommandBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplCommandBundle(TestCase):
    '''
        Test cases verifying ReplCommandBundle data carrier.

        It defines:

            :methods:
                | test_bundle_initialization - Verifies valid bundle instantiation.
                | test_bundle_immutability - Verifies frozen dataclass behavior.
    '''

    def setUp(self) -> None:
        '''Sets up mock dependencies and collaborator bundle.'''
        self.mock_reader = MagicMock()
        self.mock_dispatcher = MagicMock()
        self.mock_compiler = MagicMock()
        self.mock_transmitter = MagicMock()
        self.mock_presenter = MagicMock()
        self.mock_writer = MagicMock()
        self.bundle = ReplCommandBundle(
            reader=self.mock_reader,
            writer=self.mock_writer,
            dispatcher=self.mock_dispatcher,
            compiler=self.mock_compiler,
            transmitter=self.mock_transmitter,
            presenter=self.mock_presenter,
        )

    def test_bundle_initialization(self) -> None:
        '''Verifies fields are correctly initialized.'''
        self.assertIs(self.bundle.reader, self.mock_reader)
        self.assertIs(self.bundle.writer, self.mock_writer)
        self.assertIs(self.bundle.dispatcher, self.mock_dispatcher)
        self.assertIs(self.bundle.compiler, self.mock_compiler)
        self.assertIs(self.bundle.transmitter, self.mock_transmitter)
        self.assertIs(self.bundle.presenter, self.mock_presenter)

    def test_bundle_immutability(self) -> None:
        '''Verifies bundle is frozen and fields cannot be mutated.'''
        with self.assertRaises(FrozenInstanceError):
            self.bundle.reader = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
