# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Immutable parameter bundle encapsulating dependencies for FrameStepPresenter.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.infrastructure.command.compile.inspection.framing.header.iformatter import IFrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.iformatter import IFrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.hex.iformatter import IHexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.iformatter import IPayloadDispatcherFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class StepDependencies:
    '''
        Immutable parameter bundle encapsulating collaborator dependencies for FrameStepPresenter.

        It defines:

            :attributes:
                | header_formatter - Injected wire header formatter.
                | payload_formatter - Injected payload dispatcher formatter.
                | trailer_formatter - Injected frame trailer formatter.
                | hex_formatter - Injected raw bytes hex formatter.
    '''

    header_formatter: IFrameHeaderFormatter
    payload_formatter: IPayloadDispatcherFormatter
    trailer_formatter: IFrameTrailerFormatter
    hex_formatter: IHexStreamFormatter
