# -*- coding: UTF-8 -*-

'''
Module
    motion.py
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
    Concrete implementation of binary motion frame builder.
'''

from __future__ import annotations

from struct import pack
from typing import ClassVar, Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.protocol.ibinary_frame_packer import IBinaryFramePacker
from scaralang.infrastructure.protocol.binary.struct_format import BinaryStructFormat

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryMotionFrameBuilder:
    '''
        Builds joint motion binary frames using injected frame packer collaborator.

        It defines:

            :attributes:
                | JOINT_STEPS_FORMAT - Struct format for 22-byte joint step payload.
                | _packer - Injected wire frame packer service port.
            :methods:
                | __init__ - Initializes builder with wire frame packer collaborator.
                | build_joint_move - Builds joint step movement frame.
                | get_version - Returns component version string.
    '''

    JOINT_STEPS_FORMAT: ClassVar[str] = str(BinaryStructFormat.JOINT_STEPS)

    _packer: IBinaryFramePacker

    def __init__(self, *, packer: IBinaryFramePacker) -> None:
        '''
            Initializes motion frame builder with wire frame packer port.

            :param packer: Injected IBinaryFramePacker instance.
            :exceptions: None.
        '''
        self._packer: Final[IBinaryFramePacker] = packer

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
            :exceptions: None.
        '''
        payload: bytes = pack(
            self.JOINT_STEPS_FORMAT,
            steps.target_j1_steps,
            steps.target_j2_steps,
            steps.target_z_steps,
            steps.target_j4_steps,
            steps.duration_us,
            steps.feedrate_scale,
        )

        return self._packer.build_frame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=seq_num,
            payload=payload,
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
