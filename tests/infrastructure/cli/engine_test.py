# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit tests for CLI adapter in infrastructure layer.
'''

from __future__ import annotations

from os.path import abspath, dirname, join
from typing import Final
from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.base.setup.bundle import BaseBundle
from ats_utilities.base.setup.factory import BaseBundleFactory
from ats_utilities.base.setup.options import BaseBundleOptions
from ats_utilities.context.factory import ContextBundleFactory
from ats_utilities.exceptions.ats_type_error import ATSTypeError
from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.infrastructure.cli.engine import CLI
from scaralang.infrastructure.cli.setup.factory import CLIBundleFactory
from scaralang.infrastructure.cli.setup.options import CLIBundleOptions

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

_INFO_FILE: Final[str] = join(
    dirname(dirname(dirname(dirname(abspath(__file__))))),
    'scaralang', 'infrastructure', 'config', 'scaralang.cfg'
)


class TestCLI(TestCase):
    '''
        Test cases verifying CLI infrastructure adapter.

        It defines:

            :methods:
                | setUp - Prepares CLI instance with real components.
                | test_cli_initialization - Verifies CLI initialization.
                | test_cli_str_representation - Verifies CLI string formatting.
                | test_cli_run_unknown_command - Verifies run() with unregistered command.
                | test_cli_run_success - Verifies run() delegating to executor.
                | test_cli_run_ats_error - Verifies run() handling ATS exceptions.
                | test_cli_run_unexpected_error - Verifies run() handling unexpected errors.
                | test_cli_run_scara_error - Verifies run() handling ScaraError.
                | test_cli_invalid_bundle - Verifies initialization error on invalid bundle.
    '''

    def setUp(self) -> None:
        '''Prepares CLI instance with real dependency bundle.'''
        base_bundle: BaseBundle = BaseBundleFactory.create_bundle(
            options=BaseBundleOptions(
                info_file=_INFO_FILE,
                use_generator=False,
                context_bundle=ContextBundleFactory.create_bundle()
            )
        )
        cli_bundle = CLIBundleFactory.create_bundle(
            options=CLIBundleOptions(parser=base_bundle.option_manager)
        )
        self.cli = CLI(bundle=cli_bundle)
        self.parser = base_bundle.option_manager

    def test_cli_initialization(self) -> None:
        '''Verifies is_initialized returns True for configured CLI.'''
        self.assertTrue(self.cli.is_initialized())

    def test_cli_str_representation(self) -> None:
        '''Verifies __str__ returns non-empty formatted representation.'''
        result = str(self.cli)
        self.assertIsInstance(result, str)
        self.assertIn('CLI', result)

    def test_cli_run_unknown_command(self) -> None:
        '''Verifies run handles command with no registered executor.'''
        self.parser.parse_command = MagicMock(return_value=('unregistered_cmd', {}))
        res = self.cli.run()
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('not found', str(res.get('stderr')))

    def test_cli_run_success(self) -> None:
        '''Verifies run successfully delegates to matched executor.'''
        self.parser.parse_command = MagicMock(return_value=('info', {'verbose': False}))
        res = self.cli.run()
        self.assertEqual(res.get('returncode'), 0)

    def test_cli_run_ats_error(self) -> None:
        '''Verifies run catches ATSValueError and returns error dict.'''
        self.parser.parse_command = MagicMock(side_effect=ATSValueError('Bad value'))
        res = self.cli.run()
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('Bad value', str(res.get('stderr')))

    def test_cli_run_unexpected_error(self) -> None:
        '''Verifies run catches standard exceptions and returns error dict.'''
        self.parser.parse_command = MagicMock(side_effect=ValueError('Unexpected error'))
        res = self.cli.run()
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('Unexpected error', str(res.get('stderr')))

    def test_cli_run_scara_error(self) -> None:
        '''Verifies run catches ScaraError exceptions and returns error dict.'''
        self.parser.parse_command = MagicMock(side_effect=ScaraError('Scara domain error'))
        res = self.cli.run()
        self.assertEqual(res.get('returncode'), 1)
        self.assertIn('Scara domain error', str(res.get('stderr')))

    def test_cli_invalid_bundle(self) -> None:
        '''Verifies constructor raises ATS exceptions on invalid bundle object.'''
        with self.assertRaises(ATSValueError):
            CLI(bundle=None)  # type: ignore[arg-type]

        with self.assertRaises(ATSTypeError):
            CLI(bundle='invalid_bundle_type')  # type: ignore[arg-type]


if __name__ == '__main__':
    main()
