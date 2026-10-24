# -*- coding: UTF-8 -*-

'''
Module
    box_validator_test.py
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
    Unit tests for BoxZoneValidator implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.syntax import ScaraSyntaxError
from scaralang.core.service.parser.commands.zone.validator.box_validator import BoxZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBoxZoneValidator(TestCase):
    '''
        Test cases verifying BoxZoneValidator parameter validation.

        It defines:

            :methods:
                | setUp - Prepares BoxZoneValidator instance.
                | test_valid_parameters - Verifies valid box parameters pass.
                | test_missing_parameter - Verifies missing key raises ScaraSyntaxError.
                | test_non_numeric_parameter - Verifies non-numeric key raises ScaraSyntaxError.
                | test_inverted_x_bounds - Verifies X_MIN >= X_MAX raises ScaraSyntaxError.
                | test_inverted_y_bounds - Verifies Y_MIN >= Y_MAX raises ScaraSyntaxError.
                | test_get_version - Verifies get_version returns version string.
    '''

    def setUp(self) -> None:
        '''
            Prepares BoxZoneValidator test fixture.

            :exceptions: None.
        '''
        self._validator = BoxZoneValidator()

    def test_valid_parameters(self) -> None:
        '''
            Verifies valid box parameters pass validation without errors.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X_MIN': 10.0,
            'X_MAX': 50.0,
            'Y_MIN': -30.0,
            'Y_MAX': 20.0,
        }
        self._validator.validate_parameters(params=params, line_num=1)

    def test_missing_parameter(self) -> None:
        '''
            Verifies missing coordinate bound raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X_MIN': 10.0,
            'X_MAX': 50.0,
            'Y_MIN': -30.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=2)

    def test_non_numeric_parameter(self) -> None:
        '''
            Verifies non-numeric parameter value raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X_MIN': 'invalid',
            'X_MAX': 50.0,
            'Y_MIN': -30.0,
            'Y_MAX': 20.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=3)

    def test_inverted_x_bounds(self) -> None:
        '''
            Verifies X_MIN >= X_MAX raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X_MIN': 50.0,
            'X_MAX': 50.0,
            'Y_MIN': -30.0,
            'Y_MAX': 20.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=4)

    def test_inverted_y_bounds(self) -> None:
        '''
            Verifies Y_MIN >= Y_MAX raises ScaraSyntaxError.

            :exceptions: None.
        '''
        params: dict[str, object] = {
            'X_MIN': 10.0,
            'X_MAX': 50.0,
            'Y_MIN': 30.0,
            'Y_MAX': 20.0,
        }
        with self.assertRaises(ScaraSyntaxError):
            self._validator.validate_parameters(params=params, line_num=5)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns implementation version string.

            :exceptions: None.
        '''
        self.assertEqual(self._validator.get_version(), __version__)


if __name__ == '__main__':
    main()
