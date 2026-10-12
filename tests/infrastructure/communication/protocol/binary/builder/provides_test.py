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
    Unit tests for BuilderProvides dataclass container.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.builder import BinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.provides import BuilderProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBuilderProvides(TestCase):
    '''
        Test cases verifying BuilderProvides dataclass.

        It defines:

            :methods:
                | test_builder_provides_attributes - Verifies attributes and typing.
                | test_builder_provides_immutability - Verifies frozen behavior.
    '''

    def test_builder_provides_attributes(self) -> None:
        '''
            Tests BuilderProvides holds valid IBinaryFrameBuilder instance.
        '''
        builder = BinaryFrameBuilder()
        provides = BuilderProvides(builder=builder)
        self.assertIs(provides.builder, builder)
        self.assertIsInstance(provides.builder, IBinaryFrameBuilder)

    def test_builder_provides_immutability(self) -> None:
        '''
            Tests BuilderProvides is frozen and immutable.
        '''
        builder = BinaryFrameBuilder()
        provides = BuilderProvides(builder=builder)
        with self.assertRaises(AttributeError):
            provides.builder = builder  # type: ignore[misc]


if __name__ == '__main__':
    main()
