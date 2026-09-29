# -*- coding: UTF-8 -*-

'''
Module
    ifeedrate_validator_test.py
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
    Unit tests for IFeedrateValidator protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.trajectory.validation.feedrate.feedrate_validator import FeedrateValidator
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIFeedrateValidator(TestCase):
    '''
        Test cases verifying IFeedrateValidator structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies FeedrateValidator satisfies protocol.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that FeedrateValidator satisfies IFeedrateValidator.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        validator = FeedrateValidator(bounds=bounds)
        self.assertIsInstance(validator, IFeedrateValidator)

    def test_validator_name(self) -> None:
        '''
            Verifies that validator provides expected name identifier.
        '''
        bounds = DefaultScaraProfile.create_bounds()
        validator = FeedrateValidator(bounds=bounds)
        self.assertEqual(validator.name, 'feedrate_validator')


if __name__ == '__main__':
    main()
