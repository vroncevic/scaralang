# -*- coding: UTF-8 -*-

'''
Module
    control_command_compiler_factory.py
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
    Factory providing creation of ControlCommandCompiler components.
'''

from __future__ import annotations

from scaralang.core.service.compiler.primitive.control.control_command_compiler import ControlCommandCompiler
from scaralang.core.service.compiler.primitive.control.control_waypoint_builder_factory import ControlWaypointBuilderFactory
from scaralang.core.service.compiler.primitive.control.icontrol_waypoint_builder import IControlWaypointBuilder
from scaralang.core.service.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlCommandCompilerFactory:
    '''
        Factory providing creation of ControlCommandCompiler instances.

        It defines:

            :methods:
                | create - Instantiates ControlCommandCompiler with default collaborators.
                | create_with_builder - Instantiates ControlCommandCompiler with injected builder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> IPrimitiveCompiler:
        '''
            Creates ControlCommandCompiler with default collaborators.

            :return: Configured IPrimitiveCompiler instance.
            :exceptions: None.
        '''
        return ControlCommandCompiler(
            waypoint_builder=ControlWaypointBuilderFactory.create()
        )

    @classmethod
    def create_with_builder(
        cls,
        *,
        waypoint_builder: IControlWaypointBuilder,
    ) -> IPrimitiveCompiler:
        '''
            Creates ControlCommandCompiler with injected waypoint builder.

            :param waypoint_builder: Injected IControlWaypointBuilder collaborator.
            :return: Configured IPrimitiveCompiler instance.
            :exceptions: None.
        '''
        return ControlCommandCompiler(waypoint_builder=waypoint_builder)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
