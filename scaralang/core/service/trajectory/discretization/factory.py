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
    Factory instantiating trajectory shape discretization subsystem.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.discretization.circle.factory import CircleFactory
from scaralang.core.service.trajectory.discretization.circle.provides import CircleProvides
from scaralang.core.service.trajectory.discretization.line.factory import LineFactory
from scaralang.core.service.trajectory.discretization.line.provides import LineProvides
from scaralang.core.service.trajectory.discretization.provides import DiscretizationProvides
from scaralang.core.service.trajectory.discretization.rectangle.factory import RectangleFactory
from scaralang.core.service.trajectory.discretization.rectangle.provides import RectangleProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiscretizationFactory:
    '''
        Factory providing configured DiscretizationProvides instance.

        It defines:

            :methods:
                | create - Builds and returns DiscretizationProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> DiscretizationProvides:
        '''
            Builds and returns DiscretizationProvides bundle.

            :return: Configured DiscretizationProvides bundle instance.
            :exceptions: None.
        '''
        line_provides: LineProvides = LineFactory.create()
        circle_provides: CircleProvides = CircleFactory.create()
        rectangle_provides: RectangleProvides = RectangleFactory.create()

        return DiscretizationProvides(
            line=line_provides.discretizer,
            circle=circle_provides.discretizer,
            rectangle=rectangle_provides.discretizer,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
