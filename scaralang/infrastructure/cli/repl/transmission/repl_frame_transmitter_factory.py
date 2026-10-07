# -*- coding: UTF-8 -*-

'''
Module
    repl_frame_transmitter_factory.py
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
    Factory instantiating ReplFrameTransmitter instances.
'''

from __future__ import annotations

from scaralang.infrastructure.cli.repl.transmission.repl_frame_transmitter import ReplFrameTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplFrameTransmitterFactory:
    '''
        Factory providing ReplFrameTransmitter instances.

        It defines:

            :methods:
                | create - Builds ReplFrameTransmitter instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        endpoint: str = 'dry-run',
        dry_run: bool = True,
    ) -> ReplFrameTransmitter:
        '''
            Builds and returns a ReplFrameTransmitter instance.

            :param endpoint: Target connection endpoint identifier.
            :param dry_run: True if running in simulated dry-run mode.
            :return: Instantiated ReplFrameTransmitter instance.
            :exceptions: None.
        '''
        return ReplFrameTransmitter(endpoint=endpoint, dry_run=dry_run)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
