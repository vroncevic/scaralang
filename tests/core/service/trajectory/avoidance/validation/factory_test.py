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
    Unit tests for ValidationFactory factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.avoidance.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.avoidance.validation.provides import ValidationProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestValidationFactory(TestCase):
    '''
        Test cases for ValidationFactory creation logic.

        It defines:

            :methods:
                | test_create - Verifies factory builds ValidationProvides instance.
                | test_get_version - Verifies factory version string representation.
    '''

    def test_create(self) -> None:
        '''Verifies factory builds ValidationProvides with given radius.'''
        provides: ValidationProvides = ValidationFactory.create(dead_zone_radius=75.0)
        self.assertIsInstance(provides, ValidationProvides)
        self.assertEqual(provides.validator.get_dead_zone_radius(), 75.0)

    def test_get_version(self) -> None:
        '''Verifies factory version getter.'''
        self.assertIsInstance(ValidationFactory.get_version(), str)
        self.assertTrue(len(ValidationFactory.get_version()) > 0)


if __name__ == '__main__':
    main()
