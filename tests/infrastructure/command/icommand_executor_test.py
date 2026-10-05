# -*- coding: UTF-8 -*-

'''
Module
    icommand_executor_test.py
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
    Unit tests for ICommandExecutor protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.icommand_executor import ICommandExecutor
from scaralang.infrastructure.command.info.executor_factory import InfoCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestICommandExecutor(TestCase):
    '''
        Test cases verifying ICommandExecutor protocol conformance.

        It defines:

            :methods:
                | test_structural_conformance - Verifies that concrete executor satisfies protocol.
                | test_structural_rejection - Verifies that non-conforming class fails protocol check.
    '''

    def test_structural_conformance(self) -> None:
        '''
            Verifies that InfoCommandExecutor satisfies ICommandExecutor.
        '''
        executor = InfoCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, ICommandExecutor)

    def test_structural_rejection(self) -> None:
        '''
            Verifies that non-conforming class fails protocol check.
        '''
        class IncompleteExecutor:
            '''Dummy non-conforming class.'''

            @property
            def name(self) -> str:
                '''Returns dummy name.'''
                return 'incomplete'

            def is_ready(self) -> bool:
                '''Returns ready status.'''
                return True

        self.assertNotIsInstance(IncompleteExecutor(), ICommandExecutor)


if __name__ == '__main__':
    main()
