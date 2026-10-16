# -*- coding: UTF-8 -*-

'''
Module
    ibinary_actuator_frame_builder.py
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
    Defines IBinaryActuatorFrameBuilder protocol for tool and motor actuation frame construction.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.motor.axis_mask import AxisMask
from scaralang.core.model.protocol.binary_frame import BinaryFrame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryActuatorFrameBuilder(Protocol):
    '''
        Structural protocol defining actuator binary frame construction contracts.

        It defines:

            :methods:
                | build_tool_cmd - Builds a tool actuation command frame.
                | build_motor_config_cmd - Builds a motor configuration command frame.
                | get_version - Returns actuator frame builder version string.
    '''

    def build_tool_cmd(
        self,
        *,
        seq_num: int,
        tool_id: int,
        state: bool,
    ) -> BinaryFrame:
        '''
            Builds a tool actuation command frame (PUMP, VALVE).

            :param seq_num: Cyclic sequence index.
            :param tool_id: Tool identifier (0=PUMP, 1=VALVE).
            :param state: True to activate, False to deactivate.
            :return: Assembled tool command BinaryFrame.
        '''

    def build_motor_config_cmd(
        self,
        *,
        seq_num: int,
        mode: int,
        axis_mask: int = AxisMask.ALL,
    ) -> BinaryFrame:
        '''
            Builds a motor actuation mode configuration frame.

            :param seq_num: Cyclic sequence index.
            :param mode: Motor drive mode integer (0=OPEN_LOOP, 1=CLOSED_LOOP).
            :param axis_mask: Bitmask of target axes (default AxisMask.ALL).
            :return: Assembled motor configuration BinaryFrame.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
