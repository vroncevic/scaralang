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
    Provides container encapsulating outbound binary wire frame builder service contracts.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.imotion_builder import IBinaryMotionFrameBuilder
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class BuilderProvides:
    '''
        Immutable container providing outbound binary frame builder interfaces.

        It defines:

            :attributes:
                | packer - Bound IBinaryFramePacker service contract.
                | motion - Bound IBinaryMotionFrameBuilder service contract.
                | actuator - Bound IBinaryActuatorFrameBuilder service contract.
                | system - Bound IBinarySystemFrameBuilder service contract.
    '''

    packer: IBinaryFramePacker
    motion: IBinaryMotionFrameBuilder
    actuator: IBinaryActuatorFrameBuilder
    system: IBinarySystemFrameBuilder
