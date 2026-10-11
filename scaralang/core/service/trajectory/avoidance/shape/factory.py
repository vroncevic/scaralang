# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating ShapeProvides instances.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.avoidance.shape.dependencies import ShapeDependencies
from scaralang.core.service.trajectory.avoidance.shape.planner import AvoidanceShapePlanner
from scaralang.core.service.trajectory.avoidance.shape.provides import ShapeProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapeFactory:
    '''
        Factory providing configured ShapeProvides instances.

        It defines:

            :methods:
                | create - Builds and returns a ShapeProvides bundle from dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ShapeDependencies) -> ShapeProvides:
        '''
            Builds and returns a ShapeProvides instance from dependencies.

            :param dependencies: Injected ShapeDependencies container bundle.
            :return: Configured ShapeProvides bundle.
            :exceptions: None.
        '''
        planner = AvoidanceShapePlanner(dependencies=dependencies)
        return ShapeProvides(planner=planner)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory component version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
