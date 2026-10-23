# -*- coding: UTF-8 -*-

'''
Module
    circle_validator_test.py
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
    Unit tests for CircleZoneValidator implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.zone.validator.circle_validator import CircleZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCircleZoneValidator(TestCase):
    '''
        Test cases verifying CircleZoneValidator parameter validation.

        It defines:

            :methods:
                | setUp - Prepares CircleZoneValidator instance.
                | test_valid_parameters - Verifies valid circle parameters pass.
                | test_missing_parameter - Verifies missing key raises ScaraSyntaxError.
                | test_non_numeric_parameter - Verifies non-numeric key raises ScaraSyntaxError.
                | test_non_positive_radius - Verifies RADIUS <= 0 raises ScaraSyntaxError.
                | test_get_version - Verifies get_version returns version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares CircleZoneValidator test fixture.

            :exceptions: None.
        '''
        self._validator = CircleZoneValidator()

    def test_valid_parameters(self) -> None:
        '''
            Verifies valid circle parameters pass validation without errors.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X': 150.0,
            'Y': 50.0,
            'RADIUS': 30.0,
        }
        self._validator.validate_parameters(params=params, line_num=1)

    def test_missing_parameter(self) -> None:
        '''
            Verifies missing coordinate or radius raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X': 150.0,
            'Y': 50.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=2)

    def test_non_numeric_parameter(self) -> None:
        '''
            Verifies non-numeric parameter value raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X': 150.0,
            'Y': 'invalid',
            'RADIUS': 30.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=3)

    def test_non_positive_radius(self) -> None:
        '''
            Verifies non-positive radius raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X': 150.0,
            'Y': 50.0,
            'RADIUS': 0.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=4)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._validator.get_version(), __version__)


if __name__ == '__main__':
    main()
