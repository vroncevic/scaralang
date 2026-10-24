# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Provides container encapsulating outbound binary parser subsystem service contracts.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.iparser import IBinaryFrameParser
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker
from scaralang.core.service.protocol.isystem_unpacker import IBinarySystemPayloadUnpacker
from scaralang.infrastructure.protocol.parser.assembler.iassembler import IBinaryFrameAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ParserProvides:
    '''
        Immutable container providing outbound binary frame parser subsystem interfaces.

        It defines:

            :attributes:
                | parser - Bound IBinaryFrameParser service contract.
                | assembler - Bound IBinaryFrameAssembler service contract.
                | motion_unpacker - Bound IBinaryMotionPayloadUnpacker service contract.
                | actuator_unpacker - Bound IBinaryActuatorPayloadUnpacker service contract.
                | system_unpacker - Bound IBinarySystemPayloadUnpacker service contract.
                | response_unpacker - Bound IBinaryResponsePayloadUnpacker service contract.
    '''

    parser: IBinaryFrameParser
    assembler: IBinaryFrameAssembler
    motion_unpacker: IBinaryMotionPayloadUnpacker
    actuator_unpacker: IBinaryActuatorPayloadUnpacker
    system_unpacker: IBinarySystemPayloadUnpacker
    response_unpacker: IBinaryResponsePayloadUnpacker
