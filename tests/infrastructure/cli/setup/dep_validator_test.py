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
    Unit tests for CLIBundleDependenciesValidator class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError
from ats_utilities.option.imanager import IOptionManager

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.cli.setup.dep_validator import (
    CLIBundleDependenciesValidator,
)
from scaralang.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scaralang.infrastructure.command.command_bundle import CommandBundle
from scaralang.setup.factory import ScaralangBundleFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCLIBundleDependenciesValidator(TestCase):
    '''
        Test cases verifying CLIBundleDependenciesValidator.

        It defines:

            :methods:
                | setUp - Prepares valid dependencies for tests.
                | test_validate_success - Verifies validation with valid dependencies.
                | test_validate_none - Verifies error when dependencies is None.
                | test_validate_not_mapping - Verifies error when dependencies is not mapping.
                | test_validate_missing_attribute - Verifies error when attribute is None.
                | test_validate_invalid_type - Verifies error when attribute type is wrong.
                | test_is_valid_success - Verifies is_valid returns True on valid dependencies.
                | test_is_valid_failure - Verifies is_valid returns False on invalid dependencies.
    '''

    def setUp(self) -> None:
        '''Prepares valid dependencies from real bundle components.'''
        bundle = ScaralangBundleFactory.create_bundle()
        self.service: IScaraDslService = bundle.service
        self.parser: IOptionManager = bundle.base.option_manager
        mock_cmd = MagicMock(spec=CommandBundle)
        self.commands: tuple[CommandBundle, ...] = (mock_cmd,)
        self.valid_deps = CLIBundleDependencies(
            service=self.service,
            parser=self.parser,
            commands=self.commands
        )

    def test_validate_success(self) -> None:
        '''Verifies validate succeeds with valid dependencies.'''
        CLIBundleDependenciesValidator.validate(self.valid_deps)

    def test_validate_none(self) -> None:
        '''Verifies validate raises ATSValueError when dependencies is None.'''
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(None)  # type: ignore[arg-type]

    def test_validate_not_mapping(self) -> None:
        '''Verifies validate raises ATSTypeError when dependencies is not a mapping.'''
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate('not_mapping')  # type: ignore[arg-type]

    def test_validate_missing_attribute(self) -> None:
        '''Verifies validate raises ATSValueError when an attribute is None.'''
        invalid_deps = CLIBundleDependencies(
            service=self.service,
            parser=None,  # type: ignore[arg-type]
            commands=self.commands
        )
        with self.assertRaises(ATSValueError):
            CLIBundleDependenciesValidator.validate(invalid_deps)

    def test_validate_invalid_type(self) -> None:
        '''Verifies validate raises ATSTypeError when an attribute has invalid type.'''
        invalid_deps = CLIBundleDependencies(
            service=self.service,
            parser='invalid_parser_type',  # type: ignore[arg-type]
            commands=self.commands
        )
        with self.assertRaises(ATSTypeError):
            CLIBundleDependenciesValidator.validate(invalid_deps)

    def test_is_valid_success(self) -> None:
        '''Verifies is_valid returns True for valid dependencies.'''
        self.assertTrue(CLIBundleDependenciesValidator.is_valid(self.valid_deps))

    def test_is_valid_failure(self) -> None:
        '''Verifies is_valid returns False for invalid dependencies.'''
        self.assertFalse(CLIBundleDependenciesValidator.is_valid(None))  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
