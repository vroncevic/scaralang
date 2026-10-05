# -*- coding: UTF-8 -*-

'''
Module
    joint_steps_payload_formatter_test.py
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
    Unit tests for JointStepsPayloadFormatter service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.protocol.joint_steps import JointSteps
from scaralang.infrastructure.command.compile.inspection.framing.hex_stream_formatter import HexStreamFormatter
from scaralang.infrastructure.command.compile.inspection.payload.ijoint_steps_payload_formatter import IJointStepsPayloadFormatter
from scaralang.infrastructure.command.compile.inspection.payload.joint_steps_payload_formatter import JointStepsPayloadFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJointStepsPayloadFormatter(TestCase):
    '''Test suite verifying JointStepsPayloadFormatter formatting operations.'''

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        formatter: JointStepsPayloadFormatter = JointStepsPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        self.assertTrue(isinstance(formatter, IJointStepsPayloadFormatter))
        self.assertFalse(isinstance(object(), IJointStepsPayloadFormatter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        formatter: JointStepsPayloadFormatter = JointStepsPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        self.assertEqual(formatter.get_version(), '1.0.4')

    def test_format_joint_steps(self) -> None:
        '''Verifies formatting of joint steps coordinates and duration.'''
        formatter: JointStepsPayloadFormatter = JointStepsPayloadFormatter(
            hex_formatter=HexStreamFormatter()
        )
        steps: JointSteps = JointSteps(
            target_j1_steps=1250,
            target_j2_steps=800,
            target_z_steps=100,
            target_j4_steps=0,
            duration_us=250000,
            feedrate_scale=100,
        )
        result: str = formatter.format_joint_steps(steps=steps, raw_payload=b'\x01\x02\x03')
        self.assertIn('J1=+1250 steps', result)
        self.assertIn('J2=+800 steps', result)
        self.assertIn('Z=+100 steps', result)
        self.assertIn('J4=+0 steps', result)
        self.assertIn('Duration=250,000 µs (250.0 ms)', result)
        self.assertIn('Feedrate=100%', result)
        self.assertIn('01 02 03', result)


if __name__ == '__main__':
    main()
