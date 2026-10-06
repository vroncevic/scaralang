# -*- coding: UTF-8 -*-

'''
Module
    repl_response_presenter_test.py
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
    Unit tests for ReplResponsePresenter and ReplResponsePresenterFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.model.repl.repl_pose_state import ReplPoseState
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.infrastructure.cli.repl.presentation.irepl_response_presenter import IReplResponsePresenter
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter import ReplResponsePresenter
from scaralang.infrastructure.cli.repl.presentation.repl_response_presenter_factory import ReplResponsePresenterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplResponsePresenter(TestCase):
    '''
        Test cases verifying ReplResponsePresenter.

        It defines:

            :methods:
                | test_present_banner - Verifies welcome banner formatting.
                | test_present_success - Verifies card presentation for executed step.
                | test_present_error - Verifies error diagnostics formatting.
                | test_present_exit - Verifies session exit message.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    def test_present_banner(self) -> None:
        '''Verifies banner text content.'''
        presenter = ReplResponsePresenter()
        banner = presenter.present_banner()
        self.assertIn('SCARA Robotics Interactive Motion Console', banner)

    def test_present_success(self) -> None:
        '''Verifies success card formatting with coordinates and frame details.'''
        presenter = ReplResponsePresenter()
        frame = BinaryFrame(
            msg_id=MessageId.CMD_MOVE_JOINT_STEPS,
            seq_num=1,
            payload=b'\x00' * 22,
            crc16=0x1234,
        )
        step = Step(
            frame=frame,
            raw_bytes=b'\xAA\x55' + b'\x00' * 26 + b'\x0D',
            duration_us=250000,
            target_steps=(1000, 500, 0, 0),
            description='MOVE LINE X=100 Y=100',
            line_number=1,
        )
        context = ReplSessionContext(
            pose=ReplPoseState(current_x=100.0, current_y=100.0)
        )
        card = presenter.present_success(step=step, context=context)
        self.assertIn('Executed: MOVE LINE X=100 Y=100', card)
        self.assertIn('CMD_MOVE_JOINT_STEPS', card)
        self.assertIn('Duration: 250.0 ms', card)
        self.assertIn('X=100.00 mm', card)

    def test_present_error(self) -> None:
        '''Verifies error message formatting.'''
        presenter = ReplResponsePresenter()
        err_str = presenter.present_error(error='Invalid syntax at token FOO')
        self.assertIn('❌ Error: Invalid syntax at token FOO', err_str)

    def test_present_exit(self) -> None:
        '''Verifies session exit message.'''
        presenter = ReplResponsePresenter()
        exit_str = presenter.present_exit()
        self.assertIn('Terminating SCARA REPL session', exit_str)

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory instantiation and protocol check.'''
        presenter = ReplResponsePresenterFactory.create()
        self.assertTrue(isinstance(presenter, IReplResponsePresenter))
        self.assertEqual(ReplResponsePresenterFactory.get_version(), '1.0.6')


if __name__ == '__main__':
    main()
