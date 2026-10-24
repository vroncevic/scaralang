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
    Unit tests for SummaryFactory implementation.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.disassembler.summary.factory import SummaryFactory
from scaralang.core.service.disassembler.summary.icalculator import IDisassemblySummaryCalculator
from scaralang.core.service.disassembler.summary.provides import SummaryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSummaryFactory(TestCase):
    '''
        Test cases verifying SummaryFactory creation and versioning.

        It defines:

            :methods:
                | test_create - Verifies factory creates configured SummaryProvides.
                | test_get_version - Verifies factory version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies create returns properly configured SummaryProvides bundle.

            :exceptions: None.
        '''
        provides: SummaryProvides = SummaryFactory.create()
        self.assertIsInstance(provides, SummaryProvides)
        self.assertTrue(isinstance(provides.calculator, IDisassemblySummaryCalculator))

    def test_get_version(self) -> None:
        '''
            Verifies factory version retrieval.

            :exceptions: None.
        '''
        self.assertEqual(SummaryFactory.get_version(), '1.1.1')


if __name__ == '__main__':
    main()
