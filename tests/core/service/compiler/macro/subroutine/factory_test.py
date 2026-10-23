# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for SubroutineFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.compiler.macro.segmenter.segmenter import BlockSegmenter
from scaralang.core.service.compiler.macro.subroutine.dependencies import SubroutineDependencies
from scaralang.core.service.compiler.macro.subroutine.factory import SubroutineFactory
from scaralang.core.service.compiler.macro.subroutine.iexpander import ISubroutineExpander
from scaralang.core.service.compiler.macro.subroutine.iregistry import ISubroutineRegistry
from scaralang.core.service.compiler.macro.subroutine.provides import SubroutineProvides
from scaralang.core.service.compiler.macro.subroutine.registry import SubroutineRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SubroutineFactoryTest(TestCase):
    '''Test cases verifying SubroutineFactory assembly.'''

    def test_create_default(self) -> None:
        '''
            Verifies factory creates valid SubroutineProvides with default collaborators.

            :exceptions: None.
        '''
        provides = SubroutineFactory.create()
        self.assertIsInstance(provides, SubroutineProvides)
        self.assertIsInstance(provides.expander, ISubroutineExpander)
        self.assertIsInstance(provides.registry, ISubroutineRegistry)

    def test_create_with_dependencies(self) -> None:
        '''
            Verifies factory builds SubroutineProvides with custom injected dependencies.

            :exceptions: None.
        '''
        registry = SubroutineRegistry()
        segmenter = BlockSegmenter()
        deps = SubroutineDependencies(registry=registry, segmenter=segmenter)
        provides = SubroutineFactory.create(dependencies=deps)

        self.assertIsInstance(provides, SubroutineProvides)
        self.assertIs(provides.registry, registry)

    def test_get_version(self) -> None:
        '''
            Verifies factory version reporting.

            :exceptions: None.
        '''
        self.assertEqual(SubroutineFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
