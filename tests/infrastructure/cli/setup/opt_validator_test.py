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
    Unit tests for CLIBundleOptionsValidator class.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError
from ats_utilities.option.imanager import IOptionManager

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.cli.setup.opt_validator import (
    CLIBundleOptionsValidator,
)
from scaralang.infrastructure.cli.setup.options import CLIBundleOptions
from scaralang.setup.factory import ScaralangBundleFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleOptionsValidator(TestCase):
    '''
        Test cases verifying CLIBundleOptionsValidator.

        It defines:

            :methods:
                | setUp - Prepares valid options for tests.
                | test_validate_success - Verifies validation with valid options.
                | test_validate_none - Verifies error when options is None.
                | test_validate_not_mapping - Verifies error when options is not mapping.
                | test_validate_invalid_option_type - Verifies error when option type is wrong.
                | test_is_valid_success - Verifies is_valid returns True on valid options.
                | test_is_valid_failure - Verifies is_valid returns False on invalid options.
    '''

    def setUp(self) -> None:
        '''Prepares valid options from real bundle components.'''
        bundle = ScaralangBundleFactory.create_bundle()
        self.service: IScaraDslService = bundle.service
        self.parser: IOptionManager = bundle.base.option_manager
        self.valid_options = CLIBundleOptions(
            service=self.service,
            parser=self.parser
        )

    def test_validate_success(self) -> None:
        '''Verifies validate succeeds with valid options.'''
        CLIBundleOptionsValidator.validate(self.valid_options)

    def test_validate_none(self) -> None:
        '''Verifies validate raises ATSValueError when options is None.'''
        with self.assertRaises(ATSValueError):
            CLIBundleOptionsValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''Verifies validate raises ATSTypeError when options is not a mapping.'''
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate('not_mapping')  # type: ignore[arg-type]

    def test_validate_invalid_option_type(self) -> None:
        '''Verifies validate raises ATSTypeError when an option has invalid type.'''
        invalid_options = CLIBundleOptions(
            service='invalid_service_type',  # type: ignore[arg-type]
            parser=self.parser
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleOptionsValidator.validate(invalid_options)

    def test_is_valid_success(self) -> None:
        '''Verifies is_valid returns True for valid options.'''
        self.assertTrue(CLIBundleOptionsValidator.is_valid(self.valid_options))

    def test_is_valid_failure(self) -> None:
        '''Verifies is_valid returns False for invalid options.'''
        self.assertFalse(CLIBundleOptionsValidator.is_valid(None))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
