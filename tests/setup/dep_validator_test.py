# -*- coding: UTF-8 -*-

'''
Module
    dep_validator_test.py
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
    Unit tests for ScaralangBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaralang.setup.dep_validator import ScaralangBundleDependenciesValidator
from scaralang.setup.dependencies import ScaralangBundleDependencies
from scaralang.setup.factory import ScaralangBundleFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangBundleDependenciesValidator(TestCase):
    '''
        Test cases verifying ScaralangBundleDependenciesValidator.

        It defines:

            :methods:
                | test_validate_success - Verifies validation of properly formed dependencies.
                | test_validate_none - Verifies error when dependencies mapping is None.
                | test_validate_not_mapping - Verifies error when dependencies is not a mapping.
                | test_validate_missing_dependency - Verifies error when a dependency is missing.
                | test_validate_invalid_type - Verifies error when dependency type is wrong.
                | test_is_valid_success - Verifies is_valid returns True on valid dependencies.
                | test_is_valid_failure - Verifies is_valid returns False on invalid dependencies.
    '''

    def test_validate_success(self) -> None:
        '''Verifies valid bundle dependencies pass validation.'''
        bundle = ScaralangBundleFactory.create_bundle()
        deps: ScaralangBundleDependencies = {
            'base': bundle.base,
            'cli': bundle.cli,
        }
        ScaralangBundleDependenciesValidator.validate(dependencies=deps)

    def test_validate_none(self) -> None:
        '''Verifies validate raises ATSValueError when dependencies is None.'''
        with self.assertRaises(ATSValueError):
            ScaralangBundleDependenciesValidator.validate(dependencies=None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''Verifies validate raises ATSTypeError when dependencies is not a mapping.'''
        with self.assertRaises(ATSTypeError):
            ScaralangBundleDependenciesValidator.validate(dependencies='invalid')  # type: ignore[arg-type]

    def test_validate_missing_dependency(self) -> None:
        '''Verifies validate raises ATSValueError when a required dependency is missing.'''
        incomplete_deps: ScaralangBundleDependencies = {
            'base': MagicMock(spec=BaseBundle),
            # 'cli' is missing
        }  # type: ignore[typeddict-item]
        with self.assertRaises(ATSValueError):
            ScaralangBundleDependenciesValidator.validate(dependencies=incomplete_deps)

    def test_validate_invalid_type(self) -> None:
        '''Verifies validate raises ATSTypeError when dependency has wrong type.'''
        invalid_deps: ScaralangBundleDependencies = {
            'base': MagicMock(spec=BaseBundle),
            'cli': 'not_an_icli',  # type: ignore[typeddict-item]
        }
        with self.assertRaises(ATSTypeError):
            ScaralangBundleDependenciesValidator.validate(dependencies=invalid_deps)

    def test_is_valid_success(self) -> None:
        '''Verifies is_valid returns True for valid dependencies.'''
        bundle = ScaralangBundleFactory.create_bundle()
        deps: ScaralangBundleDependencies = {
            'base': bundle.base,
            'cli': bundle.cli,
        }
        self.assertTrue(ScaralangBundleDependenciesValidator.is_valid(dependencies=deps))

    def test_is_valid_failure(self) -> None:
        '''Verifies is_valid returns False for None or invalid dependencies.'''
        self.assertFalse(ScaralangBundleDependenciesValidator.is_valid(dependencies=None))  # type: ignore[arg-type]
        self.assertFalse(ScaralangBundleDependenciesValidator.is_valid(dependencies='bad'))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
