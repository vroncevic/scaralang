# -*- coding: UTF-8 -*-

'''
Module
    waypoint_step_dispatcher_factory.py
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
    Factory instantiating and wiring WaypointStepDispatcher instances.
'''

from __future__ import annotations

from scaralang.core.service.compiler.binary.command.icommand_compiler import ICommandCompiler
from scaralang.core.service.compiler.binary.motion.imotion_compiler import IMotionCompiler
from scaralang.core.service.compiler.binary.step.iwaypoint_step_dispatcher import IWaypointStepDispatcher
from scaralang.core.service.compiler.binary.step.waypoint_step_dispatcher import WaypointStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointStepDispatcherFactory:
    '''
        Factory providing wired IWaypointStepDispatcher instances.

        It defines:

            :methods:
                | create - Builds WaypointStepDispatcher with injected compilers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        command_compiler: ICommandCompiler,
        motion_compiler: IMotionCompiler,
    ) -> IWaypointStepDispatcher:
        '''
            Builds and returns an IWaypointStepDispatcher protocol instance.

            :param command_compiler: Injected ICommandCompiler protocol instance.
            :param motion_compiler: Injected IMotionCompiler protocol instance.
            :return: Fully wired IWaypointStepDispatcher protocol instance.
            :exceptions: None.
        '''
        return WaypointStepDispatcher(
            command_compiler=command_compiler,
            motion_compiler=motion_compiler,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
