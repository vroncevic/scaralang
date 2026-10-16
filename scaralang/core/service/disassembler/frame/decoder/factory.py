# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating specialized binary frame payload decoders.
'''

from __future__ import annotations

from scaralang.core.service.disassembler.frame.decoder.actuator_decoder import ActuatorDecoder
from scaralang.core.service.disassembler.frame.decoder.idecoder import IFramePayloadDecoder
from scaralang.core.service.disassembler.frame.decoder.joint_steps_decoder import JointStepsDecoder
from scaralang.core.service.disassembler.frame.decoder.system_decoder import SystemDecoder
from scaralang.core.service.protocol.ibinary_actuator_payload_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.ibinary_motion_payload_unpacker import IBinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PayloadDecoderFactory:
    '''
        Factory instantiating specialized binary frame payload decoders.

        It defines:

            :methods:
                | create - Builds tuple of specialized IFramePayloadDecoder instances.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        motion_unpacker: IBinaryMotionPayloadUnpacker,
        actuator_unpacker: IBinaryActuatorPayloadUnpacker,
    ) -> tuple[IFramePayloadDecoder, ...]:
        '''
            Builds tuple of specialized payload decoders.

            :param motion_unpacker: Injected IBinaryMotionPayloadUnpacker protocol strategy.
            :param actuator_unpacker: Injected IBinaryActuatorPayloadUnpacker protocol strategy.
            :return: Tuple of configured IFramePayloadDecoder protocol instances.
            :exceptions: None.
        '''
        return (
            JointStepsDecoder(unpacker=motion_unpacker),
            ActuatorDecoder(unpacker=actuator_unpacker),
            SystemDecoder(unpacker=actuator_unpacker),
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string representation.

            :return: Version string representation.
            :exceptions: None.
        '''
        return __version__
