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
    Unit tests for RepeatFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.compiler.macro.repeat.dependencies import RepeatDependencies
from scaralang.core.service.compiler.macro.repeat.factory import RepeatFactory
from scaralang.core.service.compiler.macro.repeat.iexpander import IRepeatExpander
from scaralang.core.service.compiler.macro.repeat.provides import RepeatProvides
from scaralang.core.service.compiler.macro.segmenter.segmenter import BlockSegmenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RepeatFactoryTest(TestCase):
    '''Test cases verifying RepeatFactory assembly.'''

    def test_create_default(self) -> None:
        '''
            Verifies factory creates valid RepeatProvides with default collaborator.

            :exceptions: None.
        '''
        provides = RepeatFactory.create()
        self.assertIsInstance(provides, RepeatProvides)
        self.assertIsInstance(provides.expander, IRepeatExpander)

    def test_create_with_dependencies(self) -> None:
        '''
            Verifies factory builds RepeatProvides with custom injected dependencies.

            :exceptions: None.
        '''
        segmenter = BlockSegmenter()
        deps = RepeatDependencies(segmenter=segmenter)
        provides = RepeatFactory.create(dependencies=deps)

        self.assertIsInstance(provides, RepeatProvides)

    def test_get_version(self) -> None:
        '''
            Verifies factory version reporting.

            :exceptions: None.
        '''
        self.assertEqual(RepeatFactory.get_version(), '1.1.0')


if __name__ == '__main__':
    main()
