# -*- coding: UTF-8 -*-

'''
Module
    ibinary_motion_frame_builder.py
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
    Defines IBinaryMotionFrameBuilder protocol for motion binary frame construction.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IBinaryMotionFrameBuilder(Protocol):
    '''
        Structural protocol defining joint motion binary frame construction contracts.

        It defines:

            :methods:
                | build_joint_move - Builds a MSG_CMD_MOVE_JOINT_STEPS motion frame.
                | get_version - Returns motion frame builder version string.
    '''

    def build_joint_move(
        self,
        *,
        seq_num: int,
        steps: JointSteps,
    ) -> BinaryFrame:
        '''
            Builds a joint step motion frame from JointSteps model.

            :param seq_num: Cyclic sequence index.
            :param steps: JointSteps target instance.
            :return: Assembled BinaryFrame with joint move payload.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Semantic version string.
        '''
