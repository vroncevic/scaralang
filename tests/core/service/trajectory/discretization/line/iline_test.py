# -*- coding: UTF-8 -*-

'''
Module
    iline_test.py
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
    Unit tests for ILineDiscretizer protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.line.iline import ILineDiscretizer
from scaralang.core.service.trajectory.discretization.line.line import LineDiscretizer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestILineDiscretizer(TestCase):
    '''
        Test cases for ILineDiscretizer structural protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies LineDiscretizer satisfies protocol.
                | test_structural_non_conformance - Verifies object does not satisfy protocol.
                | test_line_name - Verifies name property returns expected identifier.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies concrete LineDiscretizer satisfies ILineDiscretizer protocol.

            :exceptions: None.
        '''
        discretizer = LineDiscretizer()
        self.assertIsInstance(discretizer, ILineDiscretizer)

    def test_structural_non_conformance(self) -> None:
        '''
            Verifies non-conforming object does not satisfy ILineDiscretizer protocol.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), ILineDiscretizer)

    def test_line_name(self) -> None:
        '''
            Verifies name property returns expected identifier.

            :exceptions: None.
        '''
        discretizer = LineDiscretizer()
        self.assertEqual(discretizer.name, 'line_discretizer')


if __name__ == '__main__':
    main()
