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
    Unit tests for Scaralang engine class.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from ats_utilities.exceptions.ats_value_error import ATSValueError

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.engine import Scaralang
from scaralang.setup.factory import ScaralangBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaralangEngine(TestCase):
    '''
        Test cases verifying Scaralang engine initialization and operations.

        It defines:

            :methods:
                | test_engine_initialization - Verifies engine initializes successfully.
                | test_engine_init_invalid_bundle - Verifies init handles invalid bundle.
                | test_engine_init_unexpected_error - Verifies init handles unexpected error.
                | test_engine_init_scara_error - Verifies init handles ScaraError.
                | test_process_success - Verifies process() returns True when CLI returns 0.
                | test_process_failure_returncode - Verifies process() returns False on error.
                | test_process_not_initialized - Verifies process() returns False if not ready.
                | test_process_ats_error - Verifies process() catches ATSValueError.
                | test_process_unexpected_error - Verifies process() catches unexpected error.
                | test_process_scara_error - Verifies process() catches ScaraError.
    '''

    def test_engine_initialization(self) -> None:
        '''Verifies engine initializes successfully with valid bundle.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        self.assertTrue(engine.is_initialized())

    def test_engine_init_invalid_bundle(self) -> None:
        '''Verifies engine handles validation error gracefully on invalid bundle.'''
        engine = Scaralang(bundle=None)  # type: ignore[arg-type]
        self.assertFalse(engine.is_initialized())

    @patch('scaralang.engine.ScaralangBundleValidator.validate')
    def test_engine_init_unexpected_error(self, mock_validate: MagicMock) -> None:
        '''Verifies engine handles unexpected exception during initialization.'''
        mock_validate.side_effect = RuntimeError('Initialization failed')
        engine = Scaralang(bundle=None)  # type: ignore[arg-type]
        self.assertFalse(engine.is_initialized())

    @patch('scaralang.engine.ScaralangBundleValidator.validate')
    def test_engine_init_scara_error(self, mock_validate: MagicMock) -> None:
        '''Verifies engine handles ScaraError exception during initialization.'''
        mock_validate.side_effect = ScaraError('Scara domain error')
        engine = Scaralang(bundle=None)  # type: ignore[arg-type]
        self.assertFalse(engine.is_initialized())

    def test_process_success(self) -> None:
        '''Verifies process returns True when CLI command executes with returncode 0.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._cli.run = MagicMock(  # pylint: disable=protected-access
            return_value={'returncode': 0, 'stdout': 'Compiled successfully', 'stderr': ''}
        )
        self.assertTrue(engine.process())

    def test_process_failure_returncode(self) -> None:
        '''Verifies process returns False when CLI command fails with non-zero code.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._cli.run = MagicMock(  # pylint: disable=protected-access
            return_value={'returncode': 1, 'stdout': '', 'stderr': 'Syntax error'}
        )
        self.assertFalse(engine.process())

    def test_process_not_initialized(self) -> None:
        '''Verifies process returns False when engine is marked uninitialized.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._is_initialized = False  # pylint: disable=protected-access
        self.assertFalse(engine.process())

    def test_process_ats_error(self) -> None:
        '''Verifies process catches ATSValueError and returns False.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._cli.run = MagicMock(  # pylint: disable=protected-access
            side_effect=ATSValueError('ATS validation failed')
        )
        self.assertFalse(engine.process())

    def test_process_unexpected_error(self) -> None:
        '''Verifies process catches unexpected exceptions and returns False.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._cli.run = MagicMock(  # pylint: disable=protected-access
            side_effect=RuntimeError('Execution failed')
        )
        self.assertFalse(engine.process())

    def test_process_scara_error(self) -> None:
        '''Verifies process catches ScaraError exception and returns False.'''
        bundle = ScaralangBundleFactory.create_bundle()
        engine = Scaralang(bundle=bundle)
        engine._cli.run = MagicMock(  # pylint: disable=protected-access
            side_effect=ScaraError('Domain execution failed')
        )
        self.assertFalse(engine.process())


if __name__ == '__main__':
    main()
