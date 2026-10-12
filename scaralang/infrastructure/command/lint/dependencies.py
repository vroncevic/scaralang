# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Defines collaborator dependency bundle dataclass for LintCommandExecutor.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.linter.diagnostic.iformatter import IDiagnosticFormatter
from scaralang.core.service.linter.script.ilinter import IScriptLinter
from scaralang.infrastructure.command.lint.error.ihandler import ILintErrorHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class LintDependencies:
    '''
        Bundle containing collaborator dependencies required by LintCommandExecutor.

        It defines:

            :attributes:
                | service - Injected SCARA DSL linter service protocol instance.
                | diagnostic_formatter - Injected diagnostic report formatter protocol instance.
                | error_handler - Injected lint error handler protocol instance.
            :methods: None.
    '''

    service: IScriptLinter
    diagnostic_formatter: IDiagnosticFormatter
    error_handler: ILintErrorHandler
