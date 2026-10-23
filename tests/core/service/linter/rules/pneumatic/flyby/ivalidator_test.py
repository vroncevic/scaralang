# -*- coding: UTF-8 -*-

'''
Module
    ivalidator_test.py
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
    Unit tests for IFlybyValidator protocol compliance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.linter.rules.pneumatic.flyby.ivalidator import IFlybyValidator
from scaralang.core.service.linter.rules.pneumatic.flyby.validator import FlybyValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestIFlybyValidator(TestCase):
    '''
        Test cases verifying IFlybyValidator structural subtyping.

        It defines:

            :methods:
                | test_structural_compliance - Verifies FlybyValidator satisfies protocol.
    '''

    def test_structural_compliance(self) -> None:
        '''
            Verifies that FlybyValidator satisfies IFlybyValidator.
        '''
        validator = FlybyValidator()
        self.assertIsInstance(validator, IFlybyValidator)


if __name__ == '__main__':
    main()
