# -*- coding: UTF-8 -*-

'''
Module
    icalculator_test.py
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
    Unit tests for IArcPointCalculator protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.compiler_context import CompilerContext
from scaralang.core.model.kinematics.point_2d import Point2D
from scaralang.core.model.trajectory.arc_point import ArcPoint
from scaralang.core.service.compiler.primitive.motion.arc.calculator.icalculator import IArcPointCalculator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyArcPointCalculator:
    '''
        Dummy class implementing IArcPointCalculator for protocol verification.
    '''

    def calculate_points(
        self,
        *,
        instruction: ScaraInstruction,
        context: CompilerContext,
    ) -> tuple[Sequence[ArcPoint], Point2D]:
        '''
            Dummy implementation of calculate_points.
        '''
        _ = instruction
        _ = context
        return ((), Point2D(x=0.0, y=0.0))

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.0'


class IncompleteArcPointCalculator:  # pylint: disable=too-few-public-methods
    '''
        Incomplete dummy class missing calculate_points method.
    '''

    def get_version(self) -> str:
        '''
            Dummy implementation of get_version.
        '''
        return '1.0.0'


class TestIArcPointCalculator(TestCase):
    '''
        Test cases verifying IArcPointCalculator protocol.

        It defines:

            :methods:
                | test_runtime_checkable_satisfied - Verifies conforming class satisfies protocol.
                | test_runtime_checkable_not_satisfied - Verifies incomplete class fails check.
    '''

    def test_runtime_checkable_satisfied(self) -> None:
        '''
            Verifies conforming class passes isinstance check.
        '''
        calculator = DummyArcPointCalculator()
        self.assertIsInstance(calculator, IArcPointCalculator)

    def test_runtime_checkable_not_satisfied(self) -> None:
        '''
            Verifies non-conforming class fails isinstance check.
        '''
        calculator = IncompleteArcPointCalculator()
        self.assertNotIsInstance(calculator, IArcPointCalculator)


if __name__ == '__main__':
    main()
