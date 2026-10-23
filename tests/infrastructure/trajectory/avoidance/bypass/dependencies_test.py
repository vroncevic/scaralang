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
    Unit tests for DefaultBypassDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.trajectory.avoidance.validation.validator import DeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDefaultBypassDependencies(TestCase):
    '''
        Test cases for DefaultBypassDependencies container.

        It defines:

            :methods:
                | test_default_dependencies_fields - Verifies default fields.
                | test_custom_dependencies_fields - Verifies custom fields.
    '''

    def test_default_dependencies_fields(self) -> None:
        '''
            Verifies default values on DefaultBypassDependencies.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        deps = DefaultBypassDependencies(validator=validator)
        self.assertIs(deps.validator, validator)
        self.assertEqual(deps.safety_margin_mm, 5.0)

    def test_custom_dependencies_fields(self) -> None:
        '''
            Verifies custom values on DefaultBypassDependencies.
        '''
        validator = DeadZoneValidator(dead_zone_radius=86.0)
        deps = DefaultBypassDependencies(
            validator=validator,
            safety_margin_mm=7.0,
            angular_step_rad=0.3,
        )
        self.assertIs(deps.validator, validator)
        self.assertEqual(deps.safety_margin_mm, 7.0)
        self.assertEqual(deps.angular_step_rad, 0.3)


if __name__ == '__main__':
    main()
