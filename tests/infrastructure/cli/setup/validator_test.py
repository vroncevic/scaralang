# -*- coding: UTF-8 -*-

'''
Module
    validator_test.py
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
    Unit tests for CLIBundleValidator class.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaralang.infrastructure.cli.setup.bundle import CLIBundle
from scaralang.infrastructure.cli.setup.factory import CLIBundleFactory
from scaralang.infrastructure.cli.setup.options import CLIBundleOptions
from scaralang.infrastructure.cli.setup.validator import CLIBundleValidator
from scaralang.setup.factory import ScaralangBundleFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleValidator(TestCase):
    '''
        Test cases verifying CLIBundleValidator.

        It defines:

            :methods:
                | setUp - Prepares valid bundle for tests.
                | test_validate_success - Verifies validation with valid bundle.
                | test_validate_none - Verifies error when bundle is None.
                | test_validate_not_bundle - Verifies error when bundle is not CLIBundle.
                | test_validate_none_parser - Verifies error when parser is None.
                | test_validate_none_commands - Verifies error when commands is None.
                | test_validate_invalid_parser_type - Verifies error when parser has wrong type.
                | test_validate_invalid_commands_type - Verifies error when commands has wrong type.
                | test_is_valid_success - Verifies is_valid returns True on valid bundle.
                | test_is_valid_failure - Verifies is_valid returns False on invalid bundle.
    '''

    def setUp(self) -> None:
        '''Prepares valid CLIBundle from factory.'''
        bundle = ScaralangBundleFactory.create_bundle()
        options = CLIBundleOptions(
            parser=bundle.base.option_manager
        )
        self.valid_bundle: CLIBundle = CLIBundleFactory.create_bundle(options=options)

    def test_validate_success(self) -> None:
        '''Verifies validate succeeds with valid bundle.'''
        CLIBundleValidator.validate(self.valid_bundle)

    def test_validate_none(self) -> None:
        '''Verifies validate raises ATSValueError when bundle is None.'''
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_bundle(self) -> None:
        '''Verifies validate raises ATSTypeError when bundle is not CLIBundle instance.'''
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate('not_a_bundle')  # type: ignore[arg-type]

    def test_validate_none_parser(self) -> None:
        '''Verifies validate raises ATSValueError when parser is None.'''
        invalid_bundle = CLIBundle(
            parser=None,  # type: ignore[arg-type]
            commands=self.valid_bundle.commands
        )
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(invalid_bundle)

    def test_validate_none_commands(self) -> None:
        '''Verifies validate raises ATSValueError when commands is None.'''
        invalid_bundle = CLIBundle(
            parser=self.valid_bundle.parser,
            commands=None  # type: ignore[arg-type]
        )
        with self.assertRaises(ATSValueError):
            CLIBundleValidator.validate(invalid_bundle)

    def test_validate_invalid_parser_type(self) -> None:
        '''Verifies validate raises ATSTypeError when parser has invalid type.'''
        invalid_bundle = CLIBundle(
            parser='invalid_parser_type',  # type: ignore[arg-type]
            commands=self.valid_bundle.commands
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate(invalid_bundle)

    def test_validate_invalid_commands_type(self) -> None:
        '''Verifies validate raises ATSTypeError when commands is not a Sequence.'''
        invalid_bundle = CLIBundle(
            parser=self.valid_bundle.parser,
            commands=12345  # type: ignore[arg-type]
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleValidator.validate(invalid_bundle)

    def test_is_valid_success(self) -> None:
        '''Verifies is_valid returns True for valid bundle.'''
        self.assertTrue(CLIBundleValidator.is_valid(self.valid_bundle))

    def test_is_valid_failure(self) -> None:
        '''Verifies is_valid returns False for invalid bundle.'''
        self.assertFalse(CLIBundleValidator.is_valid(None))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
