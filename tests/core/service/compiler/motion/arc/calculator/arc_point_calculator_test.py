# -*- coding: UTF-8 -*-

'''
Module
    arc_point_calculator_test.py
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
    Unit tests for ArcPointCalculator.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.compiler.compiler_pose_state import CompilerPoseState
from scaralang.core.model.dsl.compiler.compiler_speed_state import CompilerSpeedState
from scaralang.core.model.dsl.compiler.scara_compiler_context import ScaraCompilerContext
from scaralang.core.service.transformation.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.compiler.motion.arc.calculator.arc_point_calculator import ArcPointCalculator
from scaralang.core.service.compiler.motion.arc.calculator.iarc_point_calculator import IArcPointCalculator
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator_factory import ArcInterpolatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestArcPointCalculator(TestCase):
    '''
        Test cases verifying ArcPointCalculator execution.

        It defines:

            :methods:
                | setUp - Initializes calculator and mock context.
                | test_structural_conformance - Verifies protocol check.
                | test_get_version - Verifies get_version returns valid version string.
                | test_calculate_points_cw - Verifies clockwise arc calculation.
                | test_calculate_points_ccw - Verifies counter-clockwise arc calculation.
    '''

    def setUp(self) -> None:
        '''
            Prepares calculator instance and initial context.
        '''
        self.calculator = ArcPointCalculator(
            frame_transformer=FrameTransformerFactory.create(),
            arc_interpolator=ArcInterpolatorFactory.create(),
        )
        self.context = ScaraCompilerContext(
            pose=CompilerPoseState(
                current_x=100.0,
                current_y=0.0,
                current_z=10.0,
                current_phi=0.0,
            ),
            speed=CompilerSpeedState(
                current_speed=50.0,
            ),
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies structural conformance to IArcPointCalculator.
        '''
        self.assertIsInstance(self.calculator, IArcPointCalculator)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns valid version string.
        '''
        self.assertEqual(self.calculator.get_version(), '1.0.6')


    def test_calculate_points_cw(self) -> None:
        '''
            Verifies point calculation for clockwise arc.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CW,
            parameters={'X': 0.0, 'Y': 100.0, 'I': -100.0, 'J': 0.0},
            line_number=1,
            raw_text='ARC_CW X=0 Y=100 I=-100 J=0',
        )
        points, end_point = self.calculator.calculate_points(
            instruction=instruction,
            context=self.context,
        )
        self.assertGreater(len(points), 0)
        self.assertAlmostEqual(end_point.x, 0.0)
        self.assertAlmostEqual(end_point.y, 100.0)

    def test_calculate_points_ccw(self) -> None:
        '''
            Verifies point calculation for counter-clockwise arc.
        '''
        instruction = ScaraInstruction(
            command_type=ScaraCommandType.ARC_CCW,
            parameters={'X': 0.0, 'Y': 100.0, 'I': -100.0, 'J': 0.0},
            line_number=2,
            raw_text='ARC_CCW X=0 Y=100 I=-100 J=0',
        )
        points, end_point = self.calculator.calculate_points(
            instruction=instruction,
            context=self.context,
        )
        self.assertGreater(len(points), 0)
        self.assertAlmostEqual(end_point.x, 0.0)
        self.assertAlmostEqual(end_point.y, 100.0)


if __name__ == '__main__':
    main()
