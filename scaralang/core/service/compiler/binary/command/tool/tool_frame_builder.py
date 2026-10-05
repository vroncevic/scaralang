# -*- coding: UTF-8 -*-

'''
Module
    tool_frame_builder.py
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
    Implementation of IToolFrameBuilder constructing pneumatic tool binary frames.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.ast.pneumatic_state import PneumaticState
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolFrameBuilder:
    '''
        Constructs binary wire frames for pneumatic tool actuation.

        It defines:

            :attributes:
                | _frame_builder - Injected binary frame builder protocol.
            :methods:
                | __init__ - Initializes ToolFrameBuilder with frame builder.
                | build_tool_frame - Constructs binary frame for tool command.
                | get_version - Gets implementation version string.
    '''

    _frame_builder: IBinaryFrameBuilder

    def __init__(self, *, frame_builder: IBinaryFrameBuilder) -> None:
        '''
            Initializes ToolFrameBuilder with injected frame builder.

            :param frame_builder: Injected IBinaryFrameBuilder protocol.
            :exceptions: None.
        '''
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder

    def build_tool_frame(
        self,
        *,
        tool_id: ToolId,
        arg: str,
        clean: str,
        seq_num: int,
    ) -> BinaryFrame:
        '''
            Constructs binary frame for pneumatic tool actuation.

            :param tool_id: Robotic tool identifier.
            :param arg: Command argument string.
            :param clean: Clean uppercase command string.
            :param seq_num: Frame sequence counter.
            :return: Instantiated BinaryFrame.
            :exceptions: None.
        '''
        is_on: bool = (
            arg in ('1', PneumaticState.ON)
            if arg
            else ('1' in clean or PneumaticState.ON in clean)
        )

        return self._frame_builder.build_tool_cmd(
            seq_num=seq_num,
            tool_id=int(tool_id),
            state=is_on,
        )

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
