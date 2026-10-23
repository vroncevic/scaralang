# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit tests for InfoProvides container dataclass.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.idefinition import ICommandDefinition
from scaralang.infrastructure.command.iexecutor import ICommandExecutor
from scaralang.infrastructure.command.info.definition import InfoCommandDefinition
from scaralang.infrastructure.command.info.executor import InfoCommandExecutor
from scaralang.infrastructure.command.info.provides import InfoProvides
from scaralang.infrastructure.info.factory import DefaultInfoFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestInfoProvides(TestCase):
    '''
        Test cases verifying InfoProvides dataclass fields and immutability.

        It defines:

            :methods:
                | test_provides_fields - Verifies field assignment and types.
    '''

    def test_provides_fields(self) -> None:
        '''Verifies InfoProvides stores definition and executor correctly.'''
        definition = InfoCommandDefinition()
        executor = InfoCommandExecutor(
            definition=definition,
            service=DefaultInfoFactory.create(),
        )
        provides = InfoProvides(executor=executor, definition=definition)
        self.assertIs(provides.executor, executor)
        self.assertIs(provides.definition, definition)
        self.assertIsInstance(provides.executor, ICommandExecutor)
        self.assertIsInstance(provides.definition, ICommandDefinition)


if __name__ == '__main__':
    main()
