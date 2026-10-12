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
    Defines parameter dataclass for frame decompiler dependencies.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.kinematics.iservice import IKinematicsService
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class FrameDependencies:
    '''
        Parameter dataclass encapsulating dependencies for FrameDecompiler component.

        It defines:

            :attributes:
                | kinematics - Injected kinematics calculation service.
                | transmission - Injected joint step conversion strategy.
                | unpacker - Injected binary payload deserialization adapter.
            :methods: None.
    '''

    kinematics: IKinematicsService
    transmission: IJointStepTransmissionConverter
    unpacker: IBinaryPayloadUnpacker
