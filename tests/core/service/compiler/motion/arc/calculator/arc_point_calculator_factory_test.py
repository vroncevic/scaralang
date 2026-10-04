# -*- coding: UTF-8 -*-

'''
Module
    arc_point_calculator_factory_test.py
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
    Unit tests for ArcPointCalculatorFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.motion.arc.calculator.arc_point_calculator_factory import ArcPointCalculatorFactory
from scaralang.core.service.compiler.motion.arc.calculator.iarc_point_calculator import IArcPointCalculator
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator_factory import ArcInterpolatorFactory
from scaralang.core.service.transformation.frame_transformer_factory import FrameTransformerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcPointCalculatorFactory(TestCase):
    '''
        Test cases verifying ArcPointCalculatorFactory instantiation.

        It defines:

            :methods:
                | test_create - Verifies factory returns IArcPointCalculator.
                | test_create_with_collaborators - Verifies creation with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory produces IArcPointCalculator instance.
        '''
        calculator: IArcPointCalculator = ArcPointCalculatorFactory.create()
        self.assertIsInstance(calculator, IArcPointCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = ArcPointCalculatorFactory.get_version()
        self.assertTrue(bool(version))

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies creation with explicitly injected frame transformer and interpolator.
        '''
        transformer = FrameTransformerFactory.create()
        interpolator = ArcInterpolatorFactory.create()
        calculator: IArcPointCalculator = ArcPointCalculatorFactory.create_with_collaborators(
            frame_transformer=transformer,
            arc_interpolator=interpolator,
        )
        self.assertIsInstance(calculator, IArcPointCalculator)


if __name__ == '__main__':
    main()
