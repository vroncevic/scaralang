# -*- coding: UTF-8 -*-

'''
Module
    repl_session_context.py
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
    Defines immutable ReplSessionContext model tracking active state in an interactive REPL session.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from scaralang.core.model.dsl.ast.speed_mode import SpeedMode
from scaralang.core.model.dsl.ast.zone_mode import ZoneMode
from scaralang.core.model.repl.repl_pose_state import ReplPoseState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ReplSessionContext:
    '''
        Immutable data model encapsulating current robot state in an interactive session.

        It defines:

            :attributes:
                | pose - Active Cartesian pose coordinates in mm and degrees.
                | elbow_left - True if elbow is in LEFT configuration, False for RIGHT.
                | speed_mode - Active feedrate mode (RAPID or WORK).
                | zone_mode - Active corner blending mode (FINE or BLEND).
                | pump_active - True if vacuum suction pump is energized.
                | valve_active - True if release valve is energized.
    '''

    pose: ReplPoseState = field(default_factory=ReplPoseState)
    elbow_left: bool = False
    speed_mode: SpeedMode = SpeedMode.WORK
    zone_mode: ZoneMode = ZoneMode.FINE
    pump_active: bool = False
    valve_active: bool = False
