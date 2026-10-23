# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for StepProvides dataclass container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.compile.inspection.framing.header.formatter import FrameHeaderFormatter
from scaralang.infrastructure.command.compile.inspection.framing.trailer.formatter import FrameTrailerFormatter
from scaralang.infrastructure.command.compile.inspection.hex.formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.dependencies import DispatchDependencies
from scaralang.infrastructure.command.compile.inspection.payload.dispatch.formatter import PayloadDispatcherFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint.formatter import JointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.tool.formatter import ToolCommandPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.presentation.step.dependencies import StepDependencies
from scaralang.infrastructure.command.compile.inspection.presentation.step.presenter import FrameStepPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.step.provides import StepProvides
from scaralang.infrastructure.protocol.parser.unpacker.actuator import BinaryActuatorPayloadUnpacker
from scaralang.infrastructure.protocol.parser.unpacker.motion import BinaryMotionPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStepProvides(TestCase):
    '''Test suite verifying StepProvides provider container.'''

    def setUp(self) -> None:
        '''Initializes mock presenter instance.'''
        hex_fmt: HexStreamFormatter = HexStreamFormatter()
        dispatch_deps: DispatchDependencies = DispatchDependencies(
            joint_formatter=JointStepsPayloadFormatter(hex_formatter=hex_fmt),
            tool_formatter=ToolCommandPayloadFormatter(hex_formatter=hex_fmt),
            hex_formatter=hex_fmt,
            motion_unpacker=BinaryMotionPayloadUnpacker(),
            actuator_unpacker=BinaryActuatorPayloadUnpacker(),
        )
        step_deps: StepDependencies = StepDependencies(
            header_formatter=FrameHeaderFormatter(),
            payload_formatter=PayloadDispatcherFormatter(dependencies=dispatch_deps),
            trailer_formatter=FrameTrailerFormatter(),
            hex_formatter=hex_fmt,
        )
        self.presenter: FrameStepPresenter = FrameStepPresenter(
            dependencies=step_deps
        )

    def test_provides_attributes(self) -> None:
        '''Verifies valid attribute binding on StepProvides.'''
        provides: StepProvides = StepProvides(presenter=self.presenter)
        self.assertIs(provides.presenter, self.presenter)

    def test_provides_immutability(self) -> None:
        '''Verifies StepProvides frozen dataclass raises error on mutation.'''
        provides: StepProvides = StepProvides(presenter=self.presenter)
        with self.assertRaises(FrozenInstanceError):
            provides.presenter = self.presenter  # type: ignore[misc]


if __name__ == '__main__':
    main()
