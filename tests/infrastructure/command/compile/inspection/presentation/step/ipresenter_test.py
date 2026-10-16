# -*- coding: UTF-8 -*-

'''
Module
    ipresenter_test.py
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
    Unit tests for IFrameStepPresenter protocol.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.infrastructure.command.compile.inspection.presentation.step.ipresenter import IFrameStepPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyFrameStepPresenter:
    '''Dummy implementation satisfying IFrameStepPresenter structurally.'''

    def present_step(self, *, step: BinaryStep, index: int) -> str:
        '''Presents step.'''
        return f'{index}: {step.description}'

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.9'


class TestIFrameStepPresenter(TestCase):
    '''Test suite verifying runtime checkable behavior of IFrameStepPresenter.'''

    def test_protocol_compliance(self) -> None:
        '''Verifies structural protocol compliance.'''
        dummy: DummyFrameStepPresenter = DummyFrameStepPresenter()
        self.assertTrue(isinstance(dummy, IFrameStepPresenter))
        self.assertFalse(isinstance(object(), IFrameStepPresenter))


if __name__ == '__main__':
    main()
