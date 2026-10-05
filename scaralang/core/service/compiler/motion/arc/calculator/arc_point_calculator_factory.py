# -*- coding: UTF-8 -*-

'''
Module
    arc_point_calculator_factory.py
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
    Factory instantiating ArcPointCalculator component with dependency injection.
'''

from __future__ import annotations

from scaralang.core.service.transformation.frame_transformer_factory import FrameTransformerFactory
from scaralang.core.service.transformation.iframe_transformer import IFrameTransformer
from scaralang.core.service.compiler.motion.arc.calculator.arc_point_calculator import ArcPointCalculator
from scaralang.core.service.compiler.motion.arc.calculator.iarc_point_calculator import IArcPointCalculator
from scaralang.core.service.compiler.motion.arc.interpolation.arc_interpolator_factory import ArcInterpolatorFactory
from scaralang.core.service.compiler.motion.arc.interpolation.iarc_interpolator import IArcInterpolator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ArcPointCalculatorFactory:
    '''
        Factory providing creation of ArcPointCalculator instances.

        It defines:

            :methods:
                | create - Instantiates ArcPointCalculator with collaborator factories.
                | create_with_interpolator - Instantiates with injected arc interpolator.
                | create_with_collaborators - Instantiates with all injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IArcPointCalculator:
        '''
            Creates ArcPointCalculator instance with collaborator factories.

            :return: Configured IArcPointCalculator instance.
            :exceptions: None.
        '''
        return ArcPointCalculator(
            frame_transformer=FrameTransformerFactory.create(),
            arc_interpolator=ArcInterpolatorFactory.create(),
        )

    @classmethod
    def create_with_interpolator(
        cls,
        *,
        arc_interpolator: IArcInterpolator,
    ) -> IArcPointCalculator:
        '''
            Creates ArcPointCalculator instance with injected arc interpolator.

            :param arc_interpolator: Injected IArcInterpolator instance.
            :return: Configured IArcPointCalculator instance.
            :exceptions: None.
        '''
        return ArcPointCalculator(
            frame_transformer=FrameTransformerFactory.create(),
            arc_interpolator=arc_interpolator,
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        frame_transformer: IFrameTransformer,
        arc_interpolator: IArcInterpolator,
    ) -> IArcPointCalculator:
        '''
            Creates ArcPointCalculator instance with all injected collaborators.

            :param frame_transformer: Injected IFrameTransformer instance.
            :param arc_interpolator: Injected IArcInterpolator instance.
            :return: Configured IArcPointCalculator instance.
            :exceptions: None.
        '''
        return ArcPointCalculator(
            frame_transformer=frame_transformer,
            arc_interpolator=arc_interpolator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
