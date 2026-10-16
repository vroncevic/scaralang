# -*- coding: UTF-8 -*-

'''
Module
    tangent_heading_calculator_test.py
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
    Unit tests for TangentHeadingCalculator.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.service.compiler.primitive.motion.cartesian.itangent_heading_calculator import ITangentHeadingCalculator
from scaralang.core.service.compiler.primitive.motion.cartesian.tangent_heading_calculator import TangentHeadingCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTangentHeadingCalculator(TestCase):
    '''
        Test cases verifying TangentHeadingCalculator functionality.

        It defines:

            :methods:
                | setUp - Prepares calculator fixture.
                | test_protocol_conformance - Verifies protocol check.
                | test_get_version - Verifies version string.
                | test_calculate_tangent_angle_cardinal - Verifies angles in cardinal directions.
                | test_calculate_tangent_angle_negligible - Verifies fallback on tiny motion.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture.
        '''
        self.calculator = TangentHeadingCalculator()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural conformance to ITangentHeadingCalculator.
        '''
        self.assertIsInstance(self.calculator, ITangentHeadingCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.calculator.get_version(), '1.0.9')

    def test_calculate_tangent_angle_cardinal(self) -> None:
        '''
            Verifies tangent angle calculation along cardinal axes.
        '''
        source = Point2D(x=0.0, y=0.0)
        self.assertAlmostEqual(
            self.calculator.calculate_tangent_angle(
                source=source,
                target=Point2D(x=10.0, y=0.0),
                fallback_phi=0.0,
            ),
            0.0,
            places=4,
        )
        self.assertAlmostEqual(
            self.calculator.calculate_tangent_angle(
                source=source,
                target=Point2D(x=0.0, y=10.0),
                fallback_phi=0.0,
            ),
            90.0,
            places=4,
        )
        self.assertAlmostEqual(
            self.calculator.calculate_tangent_angle(
                source=source,
                target=Point2D(x=-10.0, y=0.0),
                fallback_phi=0.0,
            ),
            180.0,
            places=4,
        )
        self.assertAlmostEqual(
            self.calculator.calculate_tangent_angle(
                source=source,
                target=Point2D(x=0.0, y=-10.0),
                fallback_phi=0.0,
            ),
            -90.0,
            places=4,
        )

    def test_calculate_tangent_angle_negligible(self) -> None:
        '''
            Verifies fallback angle when movement distance is negligible.
        '''
        source = Point2D(x=10.0, y=20.0)
        target = Point2D(x=10.00001, y=20.00001)
        fallback = 42.5
        self.assertEqual(
            self.calculator.calculate_tangent_angle(
                source=source,
                target=target,
                fallback_phi=fallback,
            ),
            fallback,
        )


if __name__ == '__main__':
    main()
