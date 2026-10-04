# -*- coding: UTF-8 -*-

'''
Module
    repl_command_dispatcher_test.py
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
    Unit tests for ReplCommandDispatcher and ReplCommandDispatcherFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.repl.repl_pose_state import ReplPoseState
from scaralang.core.model.repl.repl_session_context import ReplSessionContext
from scaralang.infrastructure.cli.repl.dispatch.irepl_command_dispatcher import IReplCommandDispatcher
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher import ReplCommandDispatcher
from scaralang.infrastructure.cli.repl.dispatch.repl_command_dispatcher_factory import ReplCommandDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestReplCommandDispatcher(TestCase):
    '''
        Test cases verifying ReplCommandDispatcher.

        It defines:

            :methods:
                | setUp - Initializes shared dispatcher under test.
                | test_empty_line - Verifies empty line handled gracefully.
                | test_exit_commands - Verifies session termination commands.
                | test_help_commands - Verifies help reference command.
                | test_clear_commands - Verifies clear and cls screen clearing commands.
                | test_info_commands - Verifies info and specs toolchain commands.
                | test_status_and_pose_commands - Verifies state inspection commands.
                | test_unhandled_dsl_line - Verifies robotic DSL lines routed for compilation.
                | test_factory_and_protocol_conformance - Verifies factory and protocol check.
    '''

    def setUp(self) -> None:
        '''Initializes shared dispatcher under test.'''
        self.dispatcher: ReplCommandDispatcher = ReplCommandDispatcherFactory.create_default()

    def test_empty_line(self) -> None:
        '''Verifies empty line returns handled with empty message.'''
        context = ReplSessionContext()
        res = self.dispatcher.dispatch_line(line='   ', context=context)
        self.assertTrue(res.is_handled)
        self.assertFalse(res.is_exit)
        self.assertEqual(res.message, '')

    def test_exit_commands(self) -> None:
        '''Verifies exit, quit and :q terminate session.'''
        context = ReplSessionContext()
        for cmd in ('exit', 'QUIT', '  :q '):
            res = self.dispatcher.dispatch_line(line=cmd, context=context)
            self.assertTrue(res.is_exit)
            self.assertTrue(res.is_handled)

    def test_help_commands(self) -> None:
        '''Verifies help and ? display manual.'''
        context = ReplSessionContext()
        res = self.dispatcher.dispatch_line(line='help', context=context)
        self.assertFalse(res.is_exit)
        self.assertTrue(res.is_handled)
        self.assertIn('Built-in REPL Commands', res.message)
        self.assertIn('info [-v]', res.message)
        self.assertIn('clear, cls', res.message)

    def test_clear_commands(self) -> None:
        '''Verifies clear and cls emit ANSI clear sequence.'''
        context = ReplSessionContext()
        for cmd in ('clear', 'CLEAR', 'cls', '  cls '):
            res = self.dispatcher.dispatch_line(line=cmd, context=context)
            self.assertFalse(res.is_exit)
            self.assertTrue(res.is_handled)
            self.assertEqual(res.message, '\033[H\033[2J')

    def test_info_commands(self) -> None:
        '''Verifies info, specs, and verbose options return toolchain report.'''
        context = ReplSessionContext()
        for cmd in ('info', 'specs', 'catalog', 'info -v', 'info verbose'):
            res = self.dispatcher.dispatch_line(line=cmd, context=context)
            self.assertFalse(res.is_exit)
            self.assertTrue(res.is_handled)
            self.assertIn('Toolchain', res.message)

    def test_status_and_pose_commands(self) -> None:
        '''Verifies status and pose commands report coordinates and states.'''
        context = ReplSessionContext(
            pose=ReplPoseState(current_x=120.5, current_y=80.0, current_z=10.0)
        )
        status_res = self.dispatcher.dispatch_line(line='status', context=context)
        self.assertTrue(status_res.is_handled)
        self.assertIn('X=120.50', status_res.message)

        pose_res = self.dispatcher.dispatch_line(line='pose', context=context)
        self.assertTrue(pose_res.is_handled)
        self.assertIn('X=120.50 mm', pose_res.message)
        formatted_pose = self.dispatcher.format_pose(context=context)
        self.assertIn('X=120.50 mm', formatted_pose)

    def test_unhandled_dsl_line(self) -> None:
        '''Verifies motion instruction lines are not handled as built-in.'''
        context = ReplSessionContext()
        res = self.dispatcher.dispatch_line(
            line='MOVE LINE X=100 Y=100 Z=0 SPEED=100', context=context
        )
        self.assertFalse(res.is_handled)
        self.assertFalse(res.is_exit)

    def test_factory_and_protocol_conformance(self) -> None:
        '''Verifies factory instantiation and structural protocol typing.'''
        dispatcher = ReplCommandDispatcherFactory.create_default()
        self.assertTrue(isinstance(dispatcher, IReplCommandDispatcher))
        self.assertEqual(ReplCommandDispatcherFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
