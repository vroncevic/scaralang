# -*- coding: UTF-8 -*-

'''
Module
    registry_test.py
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
    Unit tests for SubroutineRegistry component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.macro.subroutine import SubroutineDefinition
from scaralang.core.model.exceptions.semantic import ScaraSemanticError
from scaralang.core.service.compiler.macro.subroutine.iregistry import ISubroutineRegistry
from scaralang.core.service.compiler.macro.subroutine.registry import SubroutineRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineRegistryTest(TestCase):
    '''Test cases verifying SubroutineRegistry storage, lookup and error cases.'''

    def test_protocol_and_version(self) -> None:
        '''
            Verifies protocol implementation and version reporting.

            :exceptions: None.
        '''
        registry = SubroutineRegistry()
        self.assertIsInstance(registry, ISubroutineRegistry)
        self.assertEqual(registry.get_version(), '1.1.1')

    def test_register_and_lookup(self) -> None:
        '''
            Verifies successful registration and retrieval of subroutine definitions.

            :exceptions: None.
        '''
        registry = SubroutineRegistry()
        sub = SubroutineDefinition(name='PICK', instructions=(), line_number=1)
        registry.register(definition=sub)

        self.assertTrue(registry.has(name='PICK'))
        self.assertTrue(registry.has(name='pick'))
        retrieved = registry.lookup(name='pick')
        self.assertIs(retrieved, sub)

    def test_duplicate_registration_raises(self) -> None:
        '''
            Verifies that registering duplicate names raises ScaraSemanticError.

            :exceptions: None.
        '''
        registry = SubroutineRegistry()
        sub = SubroutineDefinition(name='PLACE', instructions=(), line_number=5)
        registry.register(definition=sub)

        with self.assertRaises(ScaraSemanticError):
            registry.register(definition=sub)

    def test_lookup_missing_raises(self) -> None:
        '''
            Verifies that looking up an unregistered name raises ScaraSemanticError.

            :exceptions: None.
        '''
        registry = SubroutineRegistry()
        self.assertFalse(registry.has(name='NONEXISTENT'))
        with self.assertRaises(ScaraSemanticError):
            registry.lookup(name='NONEXISTENT')


if __name__ == '__main__':
    main()
