# -*- coding: UTF-8 -*-

'''
Module
    frame_step_presenter_factory.py
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
    Defines FrameStepPresenterFactory creating FrameStepPresenter instances.
'''

from __future__ import annotations

from scaralang.infrastructure.command.compile.inspection.framing.frame_header_formatter_factory import FrameHeaderFormatterFactory
from scaralang.infrastructure.command.compile.inspection.framing.frame_trailer_formatter_factory import FrameTrailerFormatterFactory
from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter_factory import HexStreamFormatterFactory
from scaralang.infrastructure.command.compile.inspection.payload.payload_dispatcher_formatter_factory import PayloadDispatcherFormatterFactory
from scaralang.infrastructure.command.compile.inspection.presentation.frame_step_presenter import FrameStepPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FrameStepPresenterFactory:
    '''
        Factory instantiating FrameStepPresenter instances.

        It defines:

            :methods:
                | create - Instantiates a new FrameStepPresenter instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> FrameStepPresenter:
        '''
            Creates a new FrameStepPresenter instance using collaborator factories.

            :return: Fully configured FrameStepPresenter instance.
        '''
        return FrameStepPresenter(
            header_formatter=FrameHeaderFormatterFactory.create(),
            payload_formatter=PayloadDispatcherFormatterFactory.create_default(),
            trailer_formatter=FrameTrailerFormatterFactory.create(),
            hex_formatter=HexStreamFormatterFactory.create(),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
