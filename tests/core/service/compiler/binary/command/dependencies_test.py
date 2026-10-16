# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for CommandDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.compiler.binary.command.dependencies import CommandDependencies
from scaralang.infrastructure.protocol.binary.builder.factory import BuilderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommandDependencies(TestCase):
    '''
        Test cases verifying CommandDependencies parameter bundle.

        It defines:

            :methods:
                | test_attributes - Verifies attributes encapsulation.
                | test_immutability - Verifies frozen dataclass behavior.
    '''

    def test_attributes(self) -> None:
        '''
            Verifies attributes on CommandDependencies.
        '''
        builder_provides = BuilderFactory.create()
        deps = CommandDependencies(
            actuator_builder=builder_provides.actuator,
            system_builder=builder_provides.system,
            frame_packer=builder_provides.packer,
        )
        self.assertIs(deps.actuator_builder, builder_provides.actuator)
        self.assertIs(deps.system_builder, builder_provides.system)
        self.assertIs(deps.frame_packer, builder_provides.packer)

    def test_immutability(self) -> None:
        '''
            Verifies CommandDependencies is frozen.
        '''
        builder_provides = BuilderFactory.create()
        deps = CommandDependencies(
            actuator_builder=builder_provides.actuator,
            system_builder=builder_provides.system,
            frame_packer=builder_provides.packer,
        )
        with self.assertRaises(AttributeError):
            deps.actuator_builder = builder_provides.actuator  # type: ignore


if __name__ == '__main__':
    main()
