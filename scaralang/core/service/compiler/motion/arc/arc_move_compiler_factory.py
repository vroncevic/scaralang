# -*- coding: UTF-8 -*-

'''
Module
    arc_move_compiler_factory.py
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
    Factory for instantiating ArcMoveCompiler components with dependency injection.
'''

from __future__ import annotations

from scaralang.core.service.compiler.motion.arc.arc_move_compiler import ArcMoveCompiler
from scaralang.core.service.compiler.motion.arc.builder.arc_waypoint_builder_factory import ArcWaypointBuilderFactory
from scaralang.core.service.compiler.motion.arc.builder.iarc_waypoint_builder import IArcWaypointBuilder
from scaralang.core.service.compiler.motion.arc.calculator.arc_point_calculator_factory import ArcPointCalculatorFactory
from scaralang.core.service.compiler.motion.arc.calculator.iarc_point_calculator import IArcPointCalculator
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator
from scaralang.core.service.compiler.motion.imotion_sub_compiler import IMotionSubCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcMoveCompilerFactory:
    '''
        Factory providing creation of ArcMoveCompiler instances.

        It defines:

            :methods:
                | create - Instantiates ArcMoveCompiler with collaborator sub-factories.
                | create_with_interpolator - Instantiates with injected arc interpolator.
                | create_with_collaborators - Instantiates with injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IMotionSubCompiler:
        '''
            Creates ArcMoveCompiler instance with collaborator sub-factories.

            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return ArcMoveCompiler(
            point_calculator=ArcPointCalculatorFactory.create(),
            waypoint_builder=ArcWaypointBuilderFactory.create(),
        )

    @classmethod
    def create_with_interpolator(
        cls,
        *,
        arc_interpolator: IArcInterpolator,
    ) -> IMotionSubCompiler:
        '''
            Creates ArcMoveCompiler instance with injected interpolator.

            :param arc_interpolator: Injected IArcInterpolator instance.
            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return ArcMoveCompiler(
            point_calculator=ArcPointCalculatorFactory.create_with_interpolator(
                arc_interpolator=arc_interpolator
            ),
            waypoint_builder=ArcWaypointBuilderFactory.create(),
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        point_calculator: IArcPointCalculator,
        waypoint_builder: IArcWaypointBuilder,
    ) -> IMotionSubCompiler:
        '''
            Creates ArcMoveCompiler instance with injected collaborators.

            :param point_calculator: Injected IArcPointCalculator instance.
            :param waypoint_builder: Injected IArcWaypointBuilder instance.
            :return: Configured IMotionSubCompiler instance.
            :exceptions: None.
        '''
        return ArcMoveCompiler(
            point_calculator=point_calculator,
            waypoint_builder=waypoint_builder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
