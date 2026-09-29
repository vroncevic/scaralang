# -*- coding: UTF-8 -*-

'''
Module
    iscara_linter_test.py
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
    Unit tests for IScaraLinter protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.linter.iscara_linter import IScaraLinter
from scaralang.core.service.linter.scara_linter import ScaraLinter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIScaraLinter(TestCase):
    '''
        Test cases verifying IScaraLinter structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies ScaraLinter satisfies IScaraLinter.
                | test_rules_property - Verifies rules property on ScaraLinter.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that ScaraLinter satisfies IScaraLinter.
        '''
        linter = ScaraLinter(rules=())
        self.assertIsInstance(linter, IScaraLinter)

    def test_rules_property(self) -> None:
        '''
            Verifies that rules property returns configured rules.
        '''
        linter = ScaraLinter(rules=())
        self.assertEqual(linter.rules, ())


if __name__ == '__main__':
    main()
