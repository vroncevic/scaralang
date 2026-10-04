# -*- coding: UTF-8 -*-

'''
Module
    singularity_margins_test.py
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
    Unit tests for pure data model SingularityMargins.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scaralang.core.model.kinematics.singularity_margins import SingularityMargins

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSingularityMargins(TestCase):
    '''Unit tests validating SingularityMargins initialization, slots, and immutability.'''

    def test_instantiation(self) -> None:
        '''Verify field values on initialization.'''
        margins = SingularityMargins(
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0,
        )
        self.assertEqual(margins.singularity_outer_margin_mm, 5.0)
        self.assertEqual(margins.singularity_inner_margin_mm, 5.0)
        self.assertEqual(margins.singularity_theta2_min_rad, 0.087266)
        self.assertEqual(margins.deadzone_r_min, 20.0)

    def test_immutability(self) -> None:
        '''Verify frozen dataclass prevents mutation.'''
        margins = SingularityMargins(
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(margins, 'deadzone_r_min', 25.0)

    def test_equality(self) -> None:
        '''Verify value-object equality semantics.'''
        margins1 = SingularityMargins(
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0,
        )
        margins2 = SingularityMargins(
            singularity_outer_margin_mm=5.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0,
        )
        margins3 = SingularityMargins(
            singularity_outer_margin_mm=6.0,
            singularity_inner_margin_mm=5.0,
            singularity_theta2_min_rad=0.087266,
            deadzone_r_min=20.0,
        )
        self.assertEqual(margins1, margins2)
        self.assertNotEqual(margins1, margins3)


if __name__ == '__main__':
    main()
