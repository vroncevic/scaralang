# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler_factory_test.py
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
    Unit tests for ArcMoveCompilerFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.motion.arc.arc_move_compiler import ArcMoveCompiler
from scaralang.core.service.compiler.motion.arc.arc_move_compiler_factory import ArcMoveCompilerFactory
from scaralang.core.service.compiler.motion.arc.builder.arc_waypoint_builder_factory import ArcWaypointBuilderFactory
from scaralang.core.service.compiler.motion.arc.calculator.arc_point_calculator_factory import ArcPointCalculatorFactory
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator_factory import ArcInterpolatorFactory
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcMoveCompilerFactory(TestCase):
    '''
        Test cases verifying ArcMoveCompilerFactory creation methods.

        It defines:

            :methods:
                | test_create - Verifies factory returns ArcMoveCompiler instance.
                | test_create_with_interpolator - Verifies creation with injected interpolator.
                | test_create_with_collaborators - Verifies creation with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies default factory creation.
        '''
        compiler: ArcMoveCompiler = ArcMoveCompilerFactory.create()
        self.assertIsInstance(compiler, ArcMoveCompiler)

    def test_create_with_interpolator(self) -> None:
        '''
            Verifies creation with explicitly injected interpolator.
        '''
        interpolator: IArcInterpolator = ArcInterpolatorFactory.create()
        compiler: ArcMoveCompiler = ArcMoveCompilerFactory.create_with_interpolator(
            arc_interpolator=interpolator
        )
        self.assertIsInstance(compiler, ArcMoveCompiler)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string is non-empty.
        '''
        version: str = ArcMoveCompilerFactory.get_version()
        self.assertTrue(bool(version))

    def test_create_with_collaborators(self) -> None:
        '''
            Verifies creation with explicitly injected point calculator and waypoint builder.
        '''
        calculator = ArcPointCalculatorFactory.create()
        builder = ArcWaypointBuilderFactory.create()
        compiler: ArcMoveCompiler = ArcMoveCompilerFactory.create_with_collaborators(
            point_calculator=calculator,
            waypoint_builder=builder,
        )
        self.assertIsInstance(compiler, ArcMoveCompiler)


if __name__ == '__main__':
    main()
