# -*- coding: UTF-8 -*-

'''
Module
    link_dimensions_test.py
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
    Unit tests for pure data model LinkDimensions.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.link_dimensions import LinkDimensions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestLinkDimensions(TestCase):
    '''Unit tests validating LinkDimensions initialization, slots, and immutability.'''

    def test_instantiation(self) -> None:
        '''Verify field values on initialization.'''
        links = LinkDimensions(l1=200.0, l2=150.0)
        self.assertEqual(links.l1, 200.0)
        self.assertEqual(links.l2, 150.0)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        links = LinkDimensions(l1=150.0, l2=150.0)
        with self.assertRaises(FrozenInstanceError):
            setattr(links, 'l1', 180.0)

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        links1 = LinkDimensions(l1=150.0, l2=150.0)
        links2 = LinkDimensions(l1=150.0, l2=150.0)
        links3 = LinkDimensions(l1=150.0, l2=120.0)
        self.assertEqual(links1, links2)
        self.assertNotEqual(links1, links3)


if __name__ == '__main__':
    main()
