# -*- coding: UTF-8 -*-

'''
Module
    tool_waypoint_builder_factory.py
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
    Factory providing creation of ToolWaypointBuilder components.
'''

from __future__ import annotations

from scaralang.core.service.compiler.primitive.tool.itool_waypoint_builder import IToolWaypointBuilder
from scaralang.core.service.compiler.primitive.tool.tool_waypoint_builder import ToolWaypointBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolWaypointBuilderFactory:
    '''
        Factory providing creation of ToolWaypointBuilder instances.

        It defines:

            :methods:
                | create - Instantiates ToolWaypointBuilder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IToolWaypointBuilder:
        '''
            Creates ToolWaypointBuilder instance.

            :return: Configured IToolWaypointBuilder instance.
            :exceptions: None.
        '''
        return ToolWaypointBuilder()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
