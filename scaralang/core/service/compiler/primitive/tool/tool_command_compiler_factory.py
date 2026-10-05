# -*- coding: UTF-8 -*-

'''
Module
    tool_command_compiler_factory.py
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
    Factory providing creation of ToolCommandCompiler components.
'''

from __future__ import annotations

from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scaralang.core.service.compiler.primitive.tool.itool_waypoint_builder import IToolWaypointBuilder
from scaralang.core.service.compiler.primitive.tool.tool_command_compiler import ToolCommandCompiler
from scaralang.core.service.compiler.primitive.tool.tool_waypoint_builder_factory import ToolWaypointBuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolCommandCompilerFactory:
    '''
        Factory providing creation of ToolCommandCompiler instances.

        It defines:

            :methods:
                | create - Instantiates ToolCommandCompiler with default collaborators.
                | create_with_builder - Instantiates ToolCommandCompiler with injected builder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IPrimitiveCompiler:
        '''
            Creates ToolCommandCompiler with default collaborators.

            :return: Configured IPrimitiveCompiler instance.
            :exceptions: None.
        '''
        return ToolCommandCompiler(
            waypoint_builder=ToolWaypointBuilderFactory.create()
        )

    @classmethod
    def create_with_builder(
        cls,
        *,
        waypoint_builder: IToolWaypointBuilder,
    ) -> IPrimitiveCompiler:
        '''
            Creates ToolCommandCompiler with injected waypoint builder.

            :param waypoint_builder: Injected IToolWaypointBuilder collaborator.
            :return: Configured IPrimitiveCompiler instance.
            :exceptions: None.
        '''
        return ToolCommandCompiler(waypoint_builder=waypoint_builder)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
