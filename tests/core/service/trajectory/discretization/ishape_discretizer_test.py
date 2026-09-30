# -*- coding: UTF-8 -*-

'''
Module
    ishape_discretizer_test.py
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
    Unit tests for IShapeDiscretizer protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.discretization.ishape_discretizer import IShapeDiscretizer
from scaralang.core.service.trajectory.discretization.shape_discretizer import ShapeDiscretizer
from scaralang.core.service.trajectory.discretization.shape_discretizer_factory import ShapeDiscretizerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIShapeDiscretizer(TestCase):
    '''
        Test cases for IShapeDiscretizer protocol structural typing.

        It defines:

            :methods:
                | test_structural_conformance - Verifies ShapeDiscretizer satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
                | test_discretizer_name_property - Verifies name property matches expectation.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete ShapeDiscretizer satisfies IShapeDiscretizer protocol.'''
        discretizer = ShapeDiscretizer()
        self.assertIsInstance(discretizer, IShapeDiscretizer)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IShapeDiscretizer.'''
        discretizer = ShapeDiscretizerFactory.create()
        self.assertIsInstance(discretizer, IShapeDiscretizer)

    def test_discretizer_name_property(self) -> None:
        '''Verifies name property returns correct identifier string.'''
        discretizer = ShapeDiscretizerFactory.create()
        self.assertEqual(discretizer.name, 'shape_discretizer')


if __name__ == '__main__':
    main()
