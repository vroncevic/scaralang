# -*- coding: UTF-8 -*-

'''
Module
    icircle_test.py
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
    Unit tests for ICircleDiscretizer protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.circle.circle import CircleDiscretizer
from scaralang.core.service.trajectory.discretization.circle.icircle import ICircleDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestICircleDiscretizer(TestCase):
    '''
        Test cases for ICircleDiscretizer structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies CircleDiscretizer satisfies protocol.
                | test_structural_non_conformance - Verifies object does not satisfy protocol.
                | test_circle_name - Verifies name property returns expected identifier.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies concrete CircleDiscretizer satisfies ICircleDiscretizer protocol.

            :exceptions: None.
        '''
        discretizer = CircleDiscretizer()
        self.assertIsInstance(discretizer, ICircleDiscretizer)

    def test_structural_non_conformance(self) -> None:
        '''
            Verifies non-conforming object does not satisfy ICircleDiscretizer protocol.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), ICircleDiscretizer)

    def test_circle_name(self) -> None:
        '''
            Verifies name property returns expected identifier.

            :exceptions: None.
        '''
        discretizer = CircleDiscretizer()
        self.assertEqual(discretizer.name, 'circle_discretizer')


if __name__ == '__main__':
    main()
