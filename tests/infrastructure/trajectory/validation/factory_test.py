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
    Unit tests for DefaultValidationFactory infrastructure factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scaralang.core.service.trajectory.validation.provides import ValidationProvides
from scaralang.infrastructure.trajectory.validation.factory import DefaultValidationFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultValidationFactory(TestCase):
    '''
        Test cases validating DefaultValidationFactory behavior.

        It defines:

            :methods:
                | test_default_factory_assembly - Verifies default composition returns provides.
                | test_default_factory_version - Verifies version string representation.
    '''

    def test_default_factory_assembly(self) -> None:
        '''Verifies default infrastructure factory returns fully wired provides bundle.'''
        output = DefaultValidationFactory.create()
        self.assertIsInstance(output, ValidationProvides)
        self.assertIsInstance(output.validator, ITrajectoryValidator)

    def test_default_factory_version(self) -> None:
        '''Verifies factory exposes standard version string.'''
        ver = DefaultValidationFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertEqual(ver, '1.0.8')


if __name__ == '__main__':
    main()
