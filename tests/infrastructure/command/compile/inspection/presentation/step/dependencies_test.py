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
    Unit tests for StepDependencies dataclass bundle.
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
from scaralang.infrastructure.communication.protocol.binary.parser.unpacker.unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStepDependencies(TestCase):
    '''Test suite verifying StepDependencies parameter bundle.'''

    def setUp(self) -> None:
        '''Initializes mock/real collaborating formatters for test bundle.'''
        hex_fmt: HexStreamFormatter = HexStreamFormatter()
        dispatch_deps: DispatchDependencies = DispatchDependencies(
            joint_formatter=JointStepsPayloadFormatter(hex_formatter=hex_fmt),
            tool_formatter=ToolCommandPayloadFormatter(hex_formatter=hex_fmt),
            hex_formatter=hex_fmt,
            unpacker=BinaryPayloadUnpacker(),
        )
        self.header_fmt: FrameHeaderFormatter = FrameHeaderFormatter()
        self.payload_fmt: PayloadDispatcherFormatter = PayloadDispatcherFormatter(
            dependencies=dispatch_deps
        )
        self.trailer_fmt: FrameTrailerFormatter = FrameTrailerFormatter()
        self.hex_fmt: HexStreamFormatter = hex_fmt

    def test_bundle_initialization(self) -> None:
        '''Verifies valid attribute binding on StepDependencies.'''
        bundle: StepDependencies = StepDependencies(
            header_formatter=self.header_fmt,
            payload_formatter=self.payload_fmt,
            trailer_formatter=self.trailer_fmt,
            hex_formatter=self.hex_fmt,
        )
        self.assertIs(bundle.header_formatter, self.header_fmt)
        self.assertIs(bundle.payload_formatter, self.payload_fmt)
        self.assertIs(bundle.trailer_formatter, self.trailer_fmt)
        self.assertIs(bundle.hex_formatter, self.hex_fmt)

    def test_bundle_immutability(self) -> None:
        '''Verifies StepDependencies frozen dataclass raises error on mutation.'''
        bundle: StepDependencies = StepDependencies(
            header_formatter=self.header_fmt,
            payload_formatter=self.payload_fmt,
            trailer_formatter=self.trailer_fmt,
            hex_formatter=self.hex_fmt,
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.header_formatter = self.header_fmt  # type: ignore[misc]


if __name__ == '__main__':
    main()
