# -*- coding: UTF-8 -*-

'''
Module
    export_error_handler_test.py
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
    Unit tests for ExportErrorHandler.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_export_error import ScaraExportError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.model.exceptions.scara_protocol_error import ScaraProtocolError
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.infrastructure.command.export.error.export_error_handler import ExportErrorHandler
from scaralang.infrastructure.command.export.error.iexport_error_handler import IExportErrorHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestExportErrorHandler(TestCase):
    '''Test cases verifying ExportErrorHandler diagnostic formatting and return codes.'''

    def setUp(self) -> None:
        '''Initializes handler instance.'''
        self.handler = ExportErrorHandler()

    def test_implements_protocol(self) -> None:
        '''Verifies structural protocol compliance.'''
        self.assertIsInstance(self.handler, IExportErrorHandler)

    def test_get_version(self) -> None:
        '''Verifies handler version string retrieval.'''
        self.assertEqual(self.handler.get_version(), '1.0.4')

    def test_format_file_missing(self) -> None:
        '''Verifies formatting of missing script file message.'''
        msg: str = self.handler.format_file_missing(path='/nonexistent/test.scara')
        self.assertEqual(
            msg,
            'export_command_executor: script file does not exist: /nonexistent/test.scara',
        )

    def test_resolve_return_code(self) -> None:
        '''Verifies return code resolution.'''
        self.assertEqual(self.handler.resolve_return_code(error=Exception('err')), 1)

    def test_format_syntax_error(self) -> None:
        '''Verifies formatting of ScaraSyntaxError.'''
        err = ScaraSyntaxError('unexpected token')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [SYNTAX] unexpected token')

    def test_format_semantic_error(self) -> None:
        '''Verifies formatting of ScaraSemanticError.'''
        err = ScaraSemanticError('undefined pallet')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [SEMANTIC] undefined pallet')

    def test_format_kinematics_error(self) -> None:
        '''Verifies formatting of ScaraKinematicsError.'''
        err = ScaraKinematicsError('point unreachable')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [KINEMATICS] point unreachable')

    def test_format_protocol_error(self) -> None:
        '''Verifies formatting of ScaraProtocolError.'''
        err = ScaraProtocolError('invalid header')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [PROTOCOL] invalid header')

    def test_format_export_error(self) -> None:
        '''Verifies formatting of ScaraExportError.'''
        err = ScaraExportError('unsupported format')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [EXPORT] unsupported format')

    def test_format_domain_error(self) -> None:
        '''Verifies formatting of generic ScaraError.'''
        err = ScaraError('domain fault')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [DOMAIN] domain fault')

    def test_format_io_error(self) -> None:
        '''Verifies formatting of OSError.'''
        err = OSError('disk full')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: [IO] disk full')

    def test_format_generic_error(self) -> None:
        '''Verifies formatting of arbitrary Exception.'''
        err = ValueError('bad value')
        msg: str = self.handler.format_error(error=err)
        self.assertEqual(msg, 'export error: bad value')


if __name__ == '__main__':
    main()
