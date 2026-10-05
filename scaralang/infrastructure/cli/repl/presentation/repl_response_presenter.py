# -*- coding: UTF-8 -*-

'''
Module
    repl_response_presenter.py
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
    Concrete implementation of REPL response presenter.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.repl.repl_session_context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ReplResponsePresenter:
    '''
        Presenter formatting cards, banners and diagnostics for interactive REPL session.

        It defines:

            :methods:
                | present_banner - Formats the welcome banner and help overview.
                | present_success - Formats the execution success card for a compiled step.
                | present_error - Formats a diagnostic or syntax error report.
                | present_exit - Formats the session termination sign-off message.
    '''

    def present_banner(self) -> str:
        '''
            Formats the welcome banner and help overview.

            :return: Multiline banner string.
            :exceptions: None.
        '''
        lines: list[str] = [
            '=' * 72,
            '  SCARA Robotics Interactive Motion Console (REPL) v1.0.2',
            '  Type \'help\' for manual, \'info\' for specifications, \'status\' for state,',
            '  \'clear\' to reset viewport, or \'exit\' / \'quit\' to terminate.',
            '=' * 72,
        ]

        return '\n'.join(lines)

    def present_success(
        self,
        *,
        step: Step,
        context: ReplSessionContext,
    ) -> str:
        '''
            Formats the execution success card for a compiled step.

            :param step: Compiled binary execution step.
            :param context: Updated session context model.
            :return: Multiline formatted success card.
            :exceptions: None.
        '''
        duration_ms = step.duration_us / 1000.0
        msg_hex = f'0x{step.frame.msg_id.value:02X}'
        msg_name = step.frame.msg_id.name
        lines: list[str] = [
            f'✅ Executed: {step.description}',
            f'   Frame: {msg_name} ({msg_hex}) | {len(step.raw_bytes)} bytes | '
            f'Duration: {duration_ms:.1f} ms',
            f'   Pose:  X={context.pose.current_x:.2f} mm | Y={context.pose.current_y:.2f} mm | '
            f'Z={context.pose.current_z:.2f} mm | Phi={context.pose.current_theta4:.2f}°',
        ]

        return '\n'.join(lines)

    def present_error(self, *, error: str) -> str:
        '''
            Formats a diagnostic or syntax error report.

            :param error: Error message text.
            :return: Formatted error string.
            :exceptions: None.
        '''
        return f'❌ Error: {error}'

    def present_exit(self) -> str:
        '''
            Formats the session termination sign-off message.

            :return: Sign-off message string.
            :exceptions: None.
        '''
        return 'Goodbye! Terminating SCARA REPL session.'
