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
    Unit tests for DeadzoneProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.kinematics.profile.deadzone.provides import DeadzoneProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDeadzoneProvides(TestCase):
    '''
        Test cases verifying DeadzoneProvides data carrier.

        It defines:

            :methods:
                | setUp - Sets up mock calculator and provides container.
                | test_provides_initialization - Verifies attributes retained.
                | test_provides_immutability - Verifies frozen dataclass behavior.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with mock calculator.

            :exceptions: None.
        '''
        self.mock_calculator = MagicMock()
        self.provides = DeadzoneProvides(calculator=self.mock_calculator)

    def test_provides_initialization(self) -> None:
        '''
            Verifies container retains calculator reference.

            :exceptions: None.
        '''
        self.assertIs(self.provides.calculator, self.mock_calculator)

    def test_provides_immutability(self) -> None:
        '''
            Verifies container enforces immutability via frozen dataclass.

            :exceptions: None.
        '''
        with self.assertRaises(FrozenInstanceError):
            self.provides.calculator = self.mock_calculator  # type: ignore[misc]


if __name__ == '__main__':
    main()
