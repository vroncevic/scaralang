# -*- coding: UTF-8 -*-

'''
Module
    idiscretizer_test.py
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

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.discretizer import ShapeDiscretizer
from scaralang.core.service.trajectory.discretization.factory import DiscretizationFactory
from scaralang.core.service.trajectory.discretization.idiscretizer import IShapeDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NonConformingDiscretizer:  # pylint: disable=too-few-public-methods
    '''Dummy class not satisfying IShapeDiscretizer protocol.'''


class TestIShapeDiscretizer(TestCase):
    '''
        Test cases for IShapeDiscretizer structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies ShapeDiscretizer satisfies protocol.
                | test_factory_return_conformance - Verifies factory returns protocol instance.
                | test_non_conforming_instance - Verifies non-conforming object rejected.
                | test_discretizer_name_property - Verifies name property matches expectation.
    '''

    def test_structural_conformance(self) -> None:
        '''Verifies concrete ShapeDiscretizer satisfies IShapeDiscretizer protocol.'''
        discretizer = ShapeDiscretizer()
        self.assertIsInstance(discretizer, IShapeDiscretizer)

    def test_factory_return_conformance(self) -> None:
        '''Verifies factory returns instance satisfying IShapeDiscretizer.'''
        provides = DiscretizationFactory.create()
        self.assertIsInstance(provides.discretizer, IShapeDiscretizer)

    def test_non_conforming_instance(self) -> None:
        '''Verifies non-conforming object is rejected by runtime_checkable protocol.'''
        dummy = NonConformingDiscretizer()
        self.assertNotIsInstance(dummy, IShapeDiscretizer)

    def test_discretizer_name_property(self) -> None:
        '''Verifies name property returns correct identifier string.'''
        discretizer = ShapeDiscretizer()
        self.assertEqual(discretizer.name, 'shape_discretizer')


if __name__ == '__main__':
    main()
