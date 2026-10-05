# -*- coding: UTF-8 -*-

'''
Module
    feedrate_validator_test.py
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
    Unit tests for FeedrateValidator feedrate checking operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.trajectory.validation_result import ValidationResult
from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.validation.feedrate.feedrate_validator import FeedrateValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFeedrateValidator(TestCase):
    '''
        Test cases verifying FeedrateValidator speed limit checking.

        It defines:

            :methods:
                | setUp - Prepares test bounds and validator instance.
                | test_validate_feedrate_valid - Verifies valid feedrate passes.
                | test_validate_feedrate_too_slow - Verifies feedrate below minimum fails.
                | test_validate_feedrate_too_fast - Verifies feedrate above maximum fails.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture with ScaraBounds and FeedrateValidator.
        '''
        bounds: ScaraBounds = DefaultScaraProfile.create_bounds()
        self.validator = FeedrateValidator(bounds=bounds)

    def test_validate_feedrate_valid(self) -> None:
        '''
            Verifies that a feedrate within limits passes validation.
        '''
        res: ValidationResult = self.validator.validate_feedrate(50.0)
        self.assertTrue(res.is_valid)

    def test_validate_feedrate_too_slow(self) -> None:
        '''
            Verifies that a feedrate below minimum fails validation.
        '''
        res: ValidationResult = self.validator.validate_feedrate(0.1)
        self.assertFalse(res.is_valid)

    def test_validate_feedrate_too_fast(self) -> None:
        '''
            Verifies that a feedrate above maximum fails validation.
        '''
        res: ValidationResult = self.validator.validate_feedrate(300.0)
        self.assertFalse(res.is_valid)


if __name__ == '__main__':
    main()
