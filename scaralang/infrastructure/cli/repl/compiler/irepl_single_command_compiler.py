# -*- coding: UTF-8 -*-

'''
Module
    irepl_single_command_compiler.py
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
    Defines IReplSingleCommandCompiler protocol for single-line DSL compilation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.repl.repl_session_context import ReplSessionContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IReplSingleCommandCompiler(Protocol):
    '''
        Protocol for parsing and compiling a single DSL instruction string.

        It defines:

            :methods:
                | compile_instruction - Compiles single instruction into step and context.
                | update_context - Computes updated session context model from plan and step.
    '''

    def compile_instruction(
        self,
        *,
        line: str,
        context: ReplSessionContext,
    ) -> tuple[BinaryFrame, Step, ReplSessionContext]:
        '''
            Compiles single DSL line into BinaryFrame, Step, and updated context.

            :param line: Single DSL instruction line.
            :param context: Active REPL session context model.
            :return: Tuple of (BinaryFrame, Step, ReplSessionContext).
            :exceptions:
                | ValueError: If syntax, kinematic limits, or validation checks fail.
        '''

    def update_context(
        self,
        *,
        line: str,
        step: Step,
        plan_waypoints: tuple[object, ...],
        context: ReplSessionContext,
    ) -> ReplSessionContext:
        '''
            Computes updated session context model from plan and step.

            :param line: Raw DSL instruction line.
            :param step: Compiled binary execution step.
            :param plan_waypoints: Waypoints generated from the plan.
            :param context: Prior active REPL session context.
            :return: Updated ReplSessionContext instance.
            :exceptions: None.
        '''
