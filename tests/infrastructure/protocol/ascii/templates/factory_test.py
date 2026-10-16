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
    Unit tests for TemplatesFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.infrastructure.protocol.ascii.templates.factory import TemplatesFactory
from scaralang.infrastructure.protocol.ascii.templates.itemplates import ICommandTemplates
from scaralang.infrastructure.protocol.ascii.templates.provides import TemplatesProvides
from scaralang.infrastructure.protocol.ascii.templates.templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTemplatesFactory(TestCase):
    '''
        Test suite verifying TemplatesFactory instantiation and versioning.

        It defines:

            :methods:
                | test_create - Verifies TemplatesProvides container creation.
                | test_structural_typing - Verifies templates satisfies ICommandTemplates.
                | test_get_version - Verifies factory semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid TemplatesProvides instance.
        '''
        provides: TemplatesProvides = TemplatesFactory.create()
        self.assertIsInstance(provides, TemplatesProvides)
        self.assertIsInstance(provides.templates, CommandTemplates)

    def test_structural_typing(self) -> None:
        '''
            Verifies created templates satisfies ICommandTemplates protocol.
        '''
        provides: TemplatesProvides = TemplatesFactory.create()
        self.assertIsInstance(provides.templates, ICommandTemplates)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns a valid semantic version string.
        '''
        version: str = TemplatesFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertGreater(len(version), 0)


if __name__ == '__main__':
    main()
