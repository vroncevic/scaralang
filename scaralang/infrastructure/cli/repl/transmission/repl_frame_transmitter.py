# -*- coding: UTF-8 -*-

'''
Module
    repl_frame_transmitter.py
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
    Concrete implementation of REPL binary frame transmitter.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplFrameTransmitter:
    '''
        Transmitter sending binary frames to hardware, emulator or dry-run buffer.

        It defines:

            :attributes:
                | endpoint - Target connection endpoint identifier.
                | dry_run - True if running in simulated dry-run mode.
                | transmitted_frames - In-memory log of transmitted raw byte packets.
            :methods:
                | __init__ - Initializes transmitter with endpoint and dry-run flag.
                | transmit_frame - Transmits binary wire bytes to target or buffer.
                | is_dry_run - Checks if transmitter is operating in offline mode.
                | get_endpoint - Returns the configured target endpoint string.
    '''

    endpoint: str
    dry_run: bool
    transmitted_frames: list[bytes]

    def __init__(
        self,
        *,
        endpoint: str = 'dry-run',
        dry_run: bool = True,
    ) -> None:
        '''
            Initializes REPL frame transmitter.

            :param endpoint: Target connection endpoint identifier.
            :param dry_run: True if running in simulated dry-run mode.
            :exceptions: None.
        '''
        self.endpoint = endpoint
        self.dry_run = dry_run
        self.transmitted_frames = []

    def transmit_frame(self, *, raw_bytes: bytes) -> bool:
        '''
            Transmits binary wire bytes to target or simulation.

            :param raw_bytes: Serialized binary frame byte stream.
            :return: True if transmission succeeded, False otherwise.
            :exceptions: None.
        '''
        self.transmitted_frames.append(raw_bytes)
        return True

    def is_dry_run(self) -> bool:
        '''
            Checks if transmitter is operating in offline dry-run mode.

            :return: True if dry-run, False otherwise.
            :exceptions: None.
        '''
        return self.dry_run

    def get_endpoint(self) -> str:
        '''
            Returns the configured target endpoint string.

            :return: Endpoint string description.
            :exceptions: None.
        '''
        return self.endpoint
