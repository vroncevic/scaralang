# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for BypassDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.bypass.arc.calculator import TangentArcCalculator
from scaralang.core.service.trajectory.avoidance.bypass.dependencies import BypassDependencies
from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBypassDependencies(TestCase):
    '''
        Test cases for BypassDependencies container.

        It defines:

            :methods:
                | test_dependencies_fields - Verifies field access on BypassDependencies.
    '''

    def test_dependencies_fields(self) -> None:
        '''
            Verifies validator, calculator, and margin fields.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        calculator = TangentArcCalculator()
        deps = BypassDependencies(
            validator=validator,
            calculator=calculator,
            safety_margin_mm=7.0,
            angular_step_rad=0.3,
        )
        self.assertIs(deps.validator, validator)
        self.assertIs(deps.calculator, calculator)
        self.assertEqual(deps.safety_margin_mm, 7.0)
        self.assertEqual(deps.angular_step_rad, 0.3)


if __name__ == '__main__':
    main()
