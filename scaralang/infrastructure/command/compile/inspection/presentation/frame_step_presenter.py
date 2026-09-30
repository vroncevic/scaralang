# -*- coding: UTF-8 -*-

'''
Module
    frame_step_presenter.py
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
    Defines FrameStepPresenter assembling comprehensive visual inspection cards for binary steps.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.step import Step
from scaralang.infrastructure.command.compile.inspection.framing.iframe_header_formatter import IFrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.iframe_trailer_formatter import IFrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.framing.ihex_stream_formatter import IHexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.ipayload_dispatcher_formatter import IPayloadDispatcherFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameStepPresenter:
    '''
        Assembles visual inspection cards for single compiled steps.

        It defines:

            :attributes:
                | _header_formatter - Injected wire header formatter.
                | _payload_formatter - Injected payload dispatcher formatter.
                | _trailer_formatter - Injected frame trailer formatter.
                | _hex_formatter - Injected raw bytes hex formatter.
            :methods:
                | __init__ - Initializes presenter with collaborating formatters.
                | present_step - Formats a single step into visual card string.
    '''

    _header_formatter: IFrameHeaderFormatter
    _payload_formatter: IPayloadDispatcherFormatter
    _trailer_formatter: IFrameTrailerFormatter
    _hex_formatter: IHexStreamFormatter

    def __init__(
        self,
        *,
        header_formatter: IFrameHeaderFormatter,
        payload_formatter: IPayloadDispatcherFormatter,
        trailer_formatter: IFrameTrailerFormatter,
        hex_formatter: IHexStreamFormatter
    ) -> None:
        '''
            Initializes FrameStepPresenter with injected formatters.

            :param header_formatter: Frame header formatter.
            :param payload_formatter: Frame payload formatter.
            :param trailer_formatter: Frame trailer formatter.
            :param hex_formatter: Hexadecimal stream formatter.
        '''
        self._header_formatter: Final[IFrameHeaderFormatter] = header_formatter
        self._payload_formatter: Final[IPayloadDispatcherFormatter] = payload_formatter
        self._trailer_formatter: Final[IFrameTrailerFormatter] = trailer_formatter
        self._hex_formatter: Final[IHexStreamFormatter] = hex_formatter

    def present_step(self, *, step: Step, index: int) -> str:
        '''
            Renders complete visual card for a single compiled Step.

            :param step: Step entity to render.
            :param index: 1-based sequential step index.
            :return: Multi-line formatted card string.
        '''
        title: str = (
            f'[Frame {index:04d}] Step #{index} | Line {step.line_number}: {step.description}'
        )
        hdr: str = self._header_formatter.format_header(
            msg_id=step.frame.msg_id,
            seq_num=step.frame.seq_num,
            payload_len=len(step.frame.payload),
        )
        hdr_line: str = f'  - Wire Header:   {hdr}'
        payload_lines: str = self._payload_formatter.format_payload(
            msg_id=step.frame.msg_id,
            payload=step.frame.payload,
        )
        trailer_line: str = self._trailer_formatter.format_trailer(crc16=step.frame.crc16)
        raw_preview: str = self._hex_formatter.format_preview(data=step.raw_bytes, max_bytes=16)
        raw_line: str = f'  - Wire Frame:    {raw_preview} ({len(step.raw_bytes)} bytes)'

        return f'{title}\n{hdr_line}\n{payload_lines}\n{trailer_line}\n{raw_line}'
