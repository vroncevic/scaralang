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
    Unit tests for CommandProvides container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.command.bundle import CommandBundle
from scaralang.infrastructure.command.info.factory import InfoFactory
from scaralang.infrastructure.command.info.provides import InfoProvides
from scaralang.infrastructure.command.provides import CommandProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandProvides(TestCase):
    '''
        Test cases verifying CommandProvides container.

        It defines:

            :methods:
                | test_provides_creation - Verifies container properties.
    '''

    def test_provides_creation(self) -> None:
        '''Verifies creating CommandProvides container.'''
        info_provides: InfoProvides = InfoFactory.create()
        bundle = CommandBundle(
            definition=info_provides.definition,
            executor=info_provides.executor,
        )
        provides = CommandProvides(commands=(bundle,))
        self.assertEqual(len(provides.commands), 1)
        self.assertIs(provides.commands[0], bundle)


if __name__ == '__main__':
    main()
