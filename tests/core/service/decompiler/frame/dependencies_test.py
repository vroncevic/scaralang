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
    Unit tests for FrameDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.service.decompiler.frame.dependencies import FrameDependencies
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter
from scaralang.core.service.protocol.iactuator_unpacker import IBinaryActuatorPayloadUnpacker
from scaralang.core.service.protocol.imotion_unpacker import IBinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFrameDependencies(TestCase):
    '''
        Test cases verifying FrameDependencies dataclass.

        It defines:

            :methods:
                | test_initialization - Verifies attributes are preserved.
                | test_immutability - Verifies frozen immutability constraint.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies FrameDependencies fields are properly assigned.

            :exceptions: None.
        '''
        mock_planar = MagicMock(spec=IPlanarKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_motion = MagicMock(spec=IBinaryMotionPayloadUnpacker)
        mock_actuator = MagicMock(spec=IBinaryActuatorPayloadUnpacker)
        deps = FrameDependencies(
            planar=mock_planar,
            transmission=mock_transmission,
            motion_unpacker=mock_motion,
            actuator_unpacker=mock_actuator,
        )
        self.assertIs(deps.planar, mock_planar)
        self.assertIs(deps.transmission, mock_transmission)
        self.assertIs(deps.motion_unpacker, mock_motion)
        self.assertIs(deps.actuator_unpacker, mock_actuator)

    def test_immutability(self) -> None:
        '''
            Verifies that modifying attributes raises FrozenInstanceError.

            :exceptions: None.
        '''
        mock_planar = MagicMock(spec=IPlanarKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_motion = MagicMock(spec=IBinaryMotionPayloadUnpacker)
        mock_actuator = MagicMock(spec=IBinaryActuatorPayloadUnpacker)
        deps = FrameDependencies(
            planar=mock_planar,
            transmission=mock_transmission,
            motion_unpacker=mock_motion,
            actuator_unpacker=mock_actuator,
        )
        with self.assertRaises(FrozenInstanceError):
            deps.planar = mock_planar  # type: ignore[misc]


if __name__ == '__main__':
    main()
