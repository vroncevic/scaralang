# -*- coding: UTF-8 -*-

'''
Module
    compiler_pose_state.py
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
    Stateful domain model tracking robot Cartesian coordinates and arm configuration during compilation.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.kinematics.elbow_config import ElbowConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, kw_only=True)
class CompilerPoseState:
    '''
        Stateful model tracking robot Cartesian coordinates and arm configuration during compilation.

        It defines:

            :attributes:
                | current_x - Current Cartesian X coordinate in mm.
                | current_y - Current Cartesian Y coordinate in mm.
                | current_z - Current Cartesian Z coordinate in mm.
                | current_phi - Current 4th axis tool orientation in degrees.
                | elbow_config - Active elbow kinematic solution (RIGHT or LEFT).
    '''

    current_x: float = 150.0
    current_y: float = 0.0
    current_z: float = 20.0
    current_phi: float = 0.0
    elbow_config: ElbowConfig = ElbowConfig.RIGHT
