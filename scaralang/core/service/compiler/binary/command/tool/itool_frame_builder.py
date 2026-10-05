# -*- coding: UTF-8 -*-

'''
Module
    itool_frame_builder.py
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
    Defines structural protocol IToolFrameBuilder for constructing pneumatic tool binary frames.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.tool_id import ToolId

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IToolFrameBuilder(Protocol):
    '''
        Structural protocol defining contracts for constructing pneumatic tool binary frames.

        It defines:

            :methods:
                | build_tool_frame - Constructs binary frame for pneumatic tool actuation.
                | get_version - Gets implementation version string.
    '''

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

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
        '''
