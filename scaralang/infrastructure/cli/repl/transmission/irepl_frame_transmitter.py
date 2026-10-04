# -*- coding: UTF-8 -*-

'''
Module
    irepl_frame_transmitter.py
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
    Defines IReplFrameTransmitter protocol for transmitting compiled wire frames.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IReplFrameTransmitter(Protocol):
    '''
        Protocol for transmitting binary frame bytes to target endpoints or dry-run streams.

        It defines:

            :methods:
                | transmit_frame - Transmits binary wire bytes to target or simulation.
                | is_dry_run - Checks if transmitter is operating in offline dry-run mode.
                | get_endpoint - Returns the configured target endpoint string.
                | configure - Updates target endpoint and dry-run mode.
    '''

    def transmit_frame(self, *, raw_bytes: bytes) -> bool:
        '''
            Transmits binary wire bytes to target or simulation.

            :param raw_bytes: Serialized binary frame byte stream.
            :return: True if transmission succeeded, False otherwise.
            :exceptions: None.
        '''

    def is_dry_run(self) -> bool:
        '''
            Checks if transmitter is operating in offline dry-run mode.

            :return: True if dry-run, False otherwise.
            :exceptions: None.
        '''

    def get_endpoint(self) -> str:
        '''
            Returns the configured target endpoint string.

            :return: Endpoint string description.
            :exceptions: None.
        '''

    def configure(self, *, endpoint: str, dry_run: bool) -> None:
        '''
            Configures the transmitter with updated endpoint and dry-run mode.

            :param endpoint: Target connection endpoint identifier.
            :param dry_run: True if running in simulated dry-run mode.
            :exceptions: None.
        '''
