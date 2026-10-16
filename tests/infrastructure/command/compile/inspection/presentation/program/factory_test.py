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
    Unit tests for ProgramFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.infrastructure.command.compile.inspection.presentation.program.factory import ProgramFactory
from scaralang.infrastructure.command.compile.inspection.presentation.program.ipresenter import IProgramInspectionPresenter
from scaralang.infrastructure.command.compile.inspection.presentation.program.provides import ProgramProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyStepPresenter:
    '''Dummy step presenter satisfying IFrameStepPresenter.'''

    def present_step(self, *, step: BinaryStep, index: int) -> str:
        '''Presents dummy step.'''
        return f'{index}: {step.description}'

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.9'


class TestProgramFactory(TestCase):
    '''Test suite verifying ProgramFactory creation and versioning.'''

    def setUp(self) -> None:
        '''Initializes mock step presenter for ProgramFactory.'''
        self.step_presenter: DummyStepPresenter = DummyStepPresenter()

    def test_create(self) -> None:
        '''Verifies create returns properly configured ProgramProvides.'''
        provides: ProgramProvides = ProgramFactory.create(
            step_presenter=self.step_presenter
        )
        self.assertIsInstance(provides, ProgramProvides)
        self.assertTrue(isinstance(provides.presenter, IProgramInspectionPresenter))

    def test_get_version(self) -> None:
        '''Verifies get_version returns valid semantic version.'''
        self.assertEqual(ProgramFactory.get_version(), '1.0.9')


if __name__ == '__main__':
    main()
