# -*- coding: UTF-8 -*-

'''
Module
    iscara_dsl_service.py
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
    Defines composite interface IScaraDslService coordinating high-level
    SCARA DSL compilation and export.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scaralang.core.service.dsl.iscara_dsl_binary_compiler import IScaraDslBinaryCompiler
from scaralang.core.service.dsl.compilation.iscara_dsl_compiler import IScaraDslCompiler
from scaralang.core.service.dsl.iscara_dsl_disassembler import IScaraDslDisassembler
from scaralang.core.service.dsl.iscara_dsl_info_provider import IScaraDslInfoProvider
from scaralang.core.service.dsl.iscara_dsl_validator import IScaraDslValidator
from scaralang.core.service.exporter.scara.iscara_plan_exporter import IScaraPlanExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraDslService(
    IScaraDslCompiler,
    IScaraDslValidator,
    IScaraPlanExporter,
    IScaraDslBinaryCompiler,
    IScaraDslDisassembler,
    IScaraDslInfoProvider,
    Protocol,
):
    '''
        High-level composite orchestration service protocol for SCARA DSL processing.

        Combines compilation, validation, linting, disassembly, binary compilation,
        and plan export contracts.

        It defines:

            :methods:
                | is_initialized - Checks if all internal components are initialized.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if all subcomponents are operational, False otherwise.
            :exceptions: None.
        '''
