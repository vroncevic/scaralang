# -*- coding: UTF-8 -*-

'''
Module
    imotion_calibration_validator_test.py
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
    Unit tests for IMotionCalibrationValidator protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.linter.rules.motion.imotion_calibration_validator import IMotionCalibrationValidator
from scaralang.core.service.linter.rules.motion.motion_calibration_validator import MotionCalibrationValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIMotionCalibrationValidator(TestCase):
    '''
        Test cases verifying IMotionCalibrationValidator structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies MotionCalibrationValidator satisfies protocol.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that MotionCalibrationValidator satisfies IMotionCalibrationValidator.
        '''
        validator = MotionCalibrationValidator()
        self.assertIsInstance(validator, IMotionCalibrationValidator)


if __name__ == '__main__':
    main()
