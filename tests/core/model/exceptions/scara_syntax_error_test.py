# -*- coding: UTF-8 -*-

'''
Module
    scara_syntax_error_test.py
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
    Unit tests for ScaraSyntaxError exception model.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraSyntaxError(TestCase):
    '''Unit tests validating ScaraSyntaxError inheritance and message propagation.'''

    def test_instantiation(self) -> None:
        '''Verify exception instantiation and string representation.'''
        err = ScaraSyntaxError('Unexpected token at line 3, col 5: FOO')
        self.assertEqual(str(err), 'Unexpected token at line 3, col 5: FOO')
        self.assertIsInstance(err, ScaraError)
        self.assertIsInstance(err, Exception)

    def test_raising_and_catching(self) -> None:
        '''Verify raising and catching as ScaraSyntaxError and ScaraError.'''
        with self.assertRaises(ScaraError) as ctx:
            raise ScaraSyntaxError('Syntax error: invalid command')
        self.assertIsInstance(ctx.exception, ScaraSyntaxError)
        self.assertEqual(str(ctx.exception), 'Syntax error: invalid command')


if __name__ == '__main__':
    main()
