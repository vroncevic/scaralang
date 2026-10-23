# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for DefaultDiscretizationFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.circle.icircle import ICircleDiscretizer
from scaralang.core.service.trajectory.discretization.line.iline import ILineDiscretizer
from scaralang.core.service.trajectory.discretization.provides import DiscretizationProvides
from scaralang.core.service.trajectory.discretization.rectangle.irectangle import IRectangleDiscretizer
from scaralang.infrastructure.trajectory.discretization.factory import DefaultDiscretizationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultDiscretizationFactory(TestCase):
    '''
        Test cases validating DefaultDiscretizationFactory behavior.

        It defines:

            :methods:
                | test_default_factory_assembly - Verifies default composition returns provides.
                | test_default_factory_version - Verifies version string representation.
    '''

    def test_default_factory_assembly(self) -> None:
        '''
            Verifies default infrastructure factory returns fully wired provides bundle.

            :exceptions: None.
        '''
        output = DefaultDiscretizationFactory.create()
        self.assertIsInstance(output, DiscretizationProvides)
        self.assertIsInstance(output.line, ILineDiscretizer)
        self.assertIsInstance(output.circle, ICircleDiscretizer)
        self.assertIsInstance(output.rectangle, IRectangleDiscretizer)
        self.assertEqual(output.line.name, 'line_discretizer')
        self.assertEqual(output.circle.name, 'circle_discretizer')
        self.assertEqual(output.rectangle.name, 'rectangle_discretizer')

    def test_default_factory_version(self) -> None:
        '''
            Verifies factory exposes standard version string.

            :exceptions: None.
        '''
        ver = DefaultDiscretizationFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertEqual(ver, '1.1.0')


if __name__ == '__main__':
    main()
