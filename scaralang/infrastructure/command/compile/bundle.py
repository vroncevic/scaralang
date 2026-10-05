# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Defines collaborator bundle dataclass for CompileCommandExecutor.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.compiler.iscara_compiler import IScaraCompiler
from scaralang.infrastructure.command.compile.error.icompile_error_handler import ICompileErrorHandler
from scaralang.infrastructure.command.compile.inspection.presentation.iprogram_inspection_presenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.compile.telemetry.icompile_telemetry_formatter import ICompileTelemetryFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class CompileCommandBundle:
    '''
        Bundle containing collaborators required by CompileCommandExecutor.

        It defines:

            :attributes:
                | compiler - Injected binary compiler service protocol instance.
                | inspection_presenter - Injected binary inspection presenter protocol instance.
                | telemetry_formatter - Injected binary telemetry formatter protocol instance.
                | error_handler - Injected compile error handler protocol instance.
            :methods: None.
    '''

    compiler: IScaraCompiler
    inspection_presenter: IProgramInspectionPresenter
    telemetry_formatter: ICompileTelemetryFormatter
    error_handler: ICompileErrorHandler
