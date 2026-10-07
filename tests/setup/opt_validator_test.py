# -*- coding: UTF-8 -*-

'''
Module
    opt_validator_test.py
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
    Unit tests for ScaralangBundleOptionsValidator class.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaralang.setup.opt_validator import ScaralangBundleOptionsValidator
from scaralang.setup.options import ScaralangBundleOptions


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangBundleOptionsValidator(TestCase):
    '''
        Test cases verifying ScaralangBundleOptionsValidator.

        It defines:

            :methods:
                | test_validate_success - Verifies valid options dictionary.
                | test_validate_none - Verifies error when options is None.
                | test_validate_not_mapping - Verifies error when options is not a mapping.
                | test_validate_invalid_attr_type - Verifies error on invalid option attribute type.
                | test_is_valid_success - Verifies is_valid returns True on valid options.
                | test_is_valid_failure - Verifies is_valid returns False on invalid input.
    '''

    def test_validate_success(self) -> None:
        '''Verifies valid options dictionary passes without error.'''
        options: ScaralangBundleOptions = {'verbose': True}
        ScaralangBundleOptionsValidator.validate(options=options)

    def test_validate_none(self) -> None:
        '''Verifies validate raises ATSValueError when options is None.'''
        with self.assertRaises(ATSValueError):
            ScaralangBundleOptionsValidator.validate(options=None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''Verifies validate raises ATSTypeError when options is not a Mapping.'''
        with self.assertRaises(ATSTypeError):
            ScaralangBundleOptionsValidator.validate(options='invalid')  # type: ignore[arg-type]

    def test_validate_invalid_attr_type(self) -> None:
        '''Verifies validate raises ATSTypeError when option attribute has wrong type.'''
        invalid_options = {'verbose': 'not_a_bool'}
        with self.assertRaises(ATSTypeError):
            ScaralangBundleOptionsValidator.validate(options=invalid_options)  # type: ignore[arg-type]

    def test_is_valid_success(self) -> None:
        '''Verifies is_valid returns True for valid options.'''
        options: ScaralangBundleOptions = {'verbose': False}
        self.assertTrue(ScaralangBundleOptionsValidator.is_valid(options=options))

    def test_is_valid_failure(self) -> None:
        '''Verifies is_valid returns False for None or invalid options.'''
        self.assertFalse(ScaralangBundleOptionsValidator.is_valid(options=None))  # type: ignore[arg-type]
        self.assertFalse(ScaralangBundleOptionsValidator.is_valid(options='invalid'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
