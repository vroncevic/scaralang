# -*- coding: UTF-8 -*-

'''
Module
    executor_factory_test.py
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
    Unit tests for InfoCommandExecutorFactory class.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.info.scara_info_provider_factory import ScaraInfoProviderFactory
from scaralang.infrastructure.command.info.definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.executor import InfoCommandExecutor
from scaralang.infrastructure.command.info.executor_factory import InfoCommandExecutorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.7'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfoCommandExecutorFactory(TestCase):
    '''
        Test cases verifying InfoCommandExecutorFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory returns default InfoCommandExecutor.
                | test_create_with_collaborators - Verifies factory builds with injected collaborators.
                | test_get_version - Verifies factory version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory returns default InfoCommandExecutor instance.'''
        executor = InfoCommandExecutorFactory.create_default()
        self.assertIsInstance(executor, InfoCommandExecutor)

    def test_create_with_collaborators(self) -> None:
        '''Verifies factory builds InfoCommandExecutor with explicit collaborators.'''
        definition = InfoCommandDefinition()
        service = ScaraInfoProviderFactory.create_default()
        executor = InfoCommandExecutorFactory.create(
            definition=definition,
            service=service,
        )
        self.assertIsInstance(executor, InfoCommandExecutor)

    def test_get_version(self) -> None:
        '''Verifies factory version returns valid string.'''
        self.assertEqual(
            InfoCommandExecutorFactory.get_version(), '1.0.7'
        )


if __name__ == '__main__':
    main()
