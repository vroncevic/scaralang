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
    Unit tests for LineProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.line.line import LineDiscretizer
from scaralang.core.service.trajectory.discretization.line.provides import LineProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLineProvides(TestCase):
    '''
        Test cases for LineProvides output bundle.

        It defines:

            :methods:
                | test_bundle_initialization - Verifies attributes initialized correctly.
                | test_bundle_immutability - Verifies FrozenInstanceError on modification.
    '''

    def test_bundle_initialization(self) -> None:
        '''
            Verifies bundle holds provided line discretizer service instance.

            :exceptions: None.
        '''
        discretizer = LineDiscretizer()
        bundle = LineProvides(discretizer=discretizer)
        self.assertIs(bundle.discretizer, discretizer)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen dataclass rejects attribute mutations.

            :exceptions: None.
        '''
        discretizer = LineDiscretizer()
        bundle = LineProvides(discretizer=discretizer)
        with self.assertRaises(FrozenInstanceError):
            bundle.discretizer = discretizer  # type: ignore[misc]


if __name__ == '__main__':
    main()
