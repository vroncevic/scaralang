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
    Unit tests for DiscretizationProvides dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.circle.circle import CircleDiscretizer
from scaralang.core.service.trajectory.discretization.line.line import LineDiscretizer
from scaralang.core.service.trajectory.discretization.provides import DiscretizationProvides
from scaralang.core.service.trajectory.discretization.rectangle.rectangle import RectangleDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDiscretizationProvides(TestCase):
    '''
        Test cases for DiscretizationProvides output bundle.

        It defines:

            :methods:
                | test_bundle_initialization - Verifies attributes initialized correctly.
                | test_bundle_immutability - Verifies FrozenInstanceError on modification.
    '''

    def test_bundle_initialization(self) -> None:
        '''
            Verifies bundle holds provided discretizer service instances.

            :exceptions: None.
        '''
        line = LineDiscretizer()
        circle = CircleDiscretizer()
        rectangle = RectangleDiscretizer()
        bundle = DiscretizationProvides(
            line=line,
            circle=circle,
            rectangle=rectangle,
        )
        self.assertIs(bundle.line, line)
        self.assertIs(bundle.circle, circle)
        self.assertIs(bundle.rectangle, rectangle)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen dataclass rejects attribute mutations.

            :exceptions: None.
        '''
        line = LineDiscretizer()
        circle = CircleDiscretizer()
        rectangle = RectangleDiscretizer()
        bundle = DiscretizationProvides(
            line=line,
            circle=circle,
            rectangle=rectangle,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.line = line  # type: ignore[misc]


if __name__ == '__main__':
    main()
