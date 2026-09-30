# -*- coding: UTF-8 -*-

'''
Module
    scara_diagnostic_formatter.py
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
    Service for formatting SCARA diagnostic findings into standardized human-readable reports.
'''

from __future__ import annotations

from scaralang.core.model.dsl.diagnostic.scara_diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.scara_diagnostic_severity import ScaraDiagnosticSeverity

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraDiagnosticFormatter:
    '''
        Domain service for formatting ScaraDiagnostic findings into report strings.

        It defines:

            :methods:
                | format_report - Formats diagnostic into report text with status indicator.
                | get_version - Returns formatter version string.
    '''

    def format_report(self, *, diagnostic: ScaraDiagnostic) -> str:
        '''
            Formats the diagnostic finding into a standardized report string.

            :param diagnostic: ScaraDiagnostic value object to format.
            :return: Formatted report text string.
        '''
        prefix: str = (
            '❌ [ERROR]'
            if diagnostic.severity == ScaraDiagnosticSeverity.ERROR
            else (
                '⚠️ [WARN]'
                if diagnostic.severity == ScaraDiagnosticSeverity.WARNING
                else 'ℹ️ [INFO]'
            )
        )

        location: str = (
            f'Line {diagnostic.line}: ' if diagnostic.line > 0 else ''
        )

        return f'{prefix} {location}[{diagnostic.code}] {diagnostic.message}'

    def get_version(self) -> str:
        '''
            Returns the formatter version string.

            :return: Formatter version string.
            :exceptions: None.
        '''
        return __version__
