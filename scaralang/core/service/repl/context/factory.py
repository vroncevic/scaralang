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
    Factory instantiating initialized ReplSessionContext instances.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.repl.pose import ReplPoseState
from scaralang.core.model.repl.context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplSessionContextFactory:
    '''
        Factory providing initialized ReplSessionContext instances.

        It defines:

            :attributes:
                | DEFAULT_POSE_X - Initial Cartesian X coordinate in mm.
                | DEFAULT_POSE_Y - Initial Cartesian Y coordinate in mm.
                | DEFAULT_POSE_Z - Initial Cartesian Z coordinate in mm.
                | DEFAULT_POSE_THETA4 - Initial wrist orientation in degrees.
            :methods:
                | create - Creates an initialized ReplSessionContext instance.
                | get_version - Returns factory version string.
    '''

    DEFAULT_POSE_X: ClassVar[float] = 0.0
    DEFAULT_POSE_Y: ClassVar[float] = 0.0
    DEFAULT_POSE_Z: ClassVar[float] = 0.0
    DEFAULT_POSE_THETA4: ClassVar[float] = 0.0

    @classmethod
    def create(cls) -> ReplSessionContext:
        '''
            Creates an initialized ReplSessionContext instance.

            :return: Initialized ReplSessionContext instance.
            :exceptions: None.
        '''
        return ReplSessionContext(
            pose=ReplPoseState(
                current_x=cls.DEFAULT_POSE_X,
                current_y=cls.DEFAULT_POSE_Y,
                current_z=cls.DEFAULT_POSE_Z,
                current_theta4=cls.DEFAULT_POSE_THETA4,
            ),
            elbow_left=False,
            speed_mode=SpeedMode.WORK,
            zone_mode=ZoneMode.FINE,
            pump_active=False,
            valve_active=False,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string representation.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
