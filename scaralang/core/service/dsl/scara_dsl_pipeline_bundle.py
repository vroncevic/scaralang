# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_pipeline_bundle.py
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
    Defines pipeline dependency bundle dataclass for ScaraDslServiceFactory.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.core.service.protocol.ibinary_payload_unpacker import IBinaryPayloadUnpacker
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraDslPipelineBundle:
    '''
        Bundle containing external pipeline dependencies required by ScaraDslServiceFactory.

        It defines:

            :attributes:
                | frame_builder - Injected IBinaryFrameBuilder protocol instance.
                | frame_parser - Injected IBinaryFrameParser protocol instance.
                | payload_unpacker - Injected IBinaryPayloadUnpacker protocol instance.
                | kinematics - Injected IKinematicsService protocol instance.
                | validator - Injected ITrajectoryValidator protocol instance.
                | transmission - Injected TransmissionParameters configuration model.
            :methods: None.
    '''

    frame_builder: IBinaryFrameBuilder
    frame_parser: IBinaryFrameParser
    payload_unpacker: IBinaryPayloadUnpacker
    kinematics: IKinematicsService
    validator: ITrajectoryValidator
    transmission: TransmissionParameters
