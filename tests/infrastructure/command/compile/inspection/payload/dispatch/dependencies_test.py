# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for DispatchDependencies dataclass container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker
from scaralang.infrastructure.command.compile.inspection.hex.iformatter import IHexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.dependencies import DispatchDependencies
from scaralang.infrastructure.command.compile.inspection.payload.joint.iformatter import IJointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool.iformatter import IToolCommandPayloadFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DispatchDependenciesTest(TestCase):
    '''
        Validates DispatchDependencies immutability and attribute accessibility.

        It defines:

            :methods:
                | test_container_attributes - Verifies dependencies container stores collaborators.
    '''

    def test_container_attributes(self) -> None:
        '''
            Verifies dependencies container properly stores and exposes collaborators.

            :exceptions: None.
        '''
        mock_joint = MagicMock(spec=IJointStepsPayloadFormatter)
        mock_tool = MagicMock(spec=IToolCommandPayloadFormatter)
        mock_hex = MagicMock(spec=IHexStreamFormatter)
        mock_motion = MagicMock(spec=IBinaryMotionPayloadUnpacker)
        mock_actuator = MagicMock(spec=IBinaryActuatorPayloadUnpacker)
        deps = DispatchDependencies(
            joint_formatter=mock_joint,
            tool_formatter=mock_tool,
            hex_formatter=mock_hex,
            motion_unpacker=mock_motion,
            actuator_unpacker=mock_actuator,
        )
        self.assertIs(deps.joint_formatter, mock_joint)
        self.assertIs(deps.tool_formatter, mock_tool)
        self.assertIs(deps.hex_formatter, mock_hex)
        self.assertIs(deps.motion_unpacker, mock_motion)
        self.assertIs(deps.actuator_unpacker, mock_actuator)


if __name__ == '__main__':
    main()
