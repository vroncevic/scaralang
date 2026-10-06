# -*- coding: UTF-8 -*-

'''
Module
    state_homing_validator_factory_test.py
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
    Unit tests for StateHomingValidatorFactory operations.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.linter.rules.state.istate_homing_validator import IStateHomingValidator
from scaralang.core.service.linter.rules.state.state_homing_validator_factory import StateHomingValidatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStateHomingValidatorFactory(TestCase):
    '''
        Test cases verifying StateHomingValidatorFactory instantiation.

        It defines:

            :methods:
                | test_create_returns_instance - Verifies factory returns IStateHomingValidator.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_returns_instance(self) -> None:
        '''
            Verifies create builds a valid IStateHomingValidator instance.
        '''
        validator = StateHomingValidatorFactory.create()
        self.assertIsInstance(validator, IStateHomingValidator)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns correct version string.
        '''
        self.assertEqual(StateHomingValidatorFactory.get_version(), '1.0.6')


if __name__ == '__main__':
    main()
