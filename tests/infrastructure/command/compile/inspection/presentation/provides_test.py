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
    Unit tests for PresentationProvides dataclass container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase
from unittest import main

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep
from scaralang.infrastructure.command.compile.inspection.presentation.provides import PresentationProvides


class DummyProgramPresenter:
    '''Dummy program presenter satisfying IProgramInspectionPresenter.'''

    def present_program(self, *, program: BinaryProgram) -> str:
        '''Presents program.'''
        return f'{len(program.steps)} steps'

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.1.0'


class DummyStepPresenter:
    '''Dummy step presenter satisfying IFrameStepPresenter.'''

    def present_step(self, *, step: BinaryStep, index: int) -> str:
        '''Presents step.'''
        return f'{index}: {step.description}'

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.1.0'


class TestPresentationProvides(TestCase):
    '''Test suite verifying PresentationProvides provider container.'''

    def setUp(self) -> None:
        '''Initializes mock presenter instances.'''
        self.program_presenter: DummyProgramPresenter = DummyProgramPresenter()
        self.step_presenter: DummyStepPresenter = DummyStepPresenter()

    def test_provides_attributes(self) -> None:
        '''Verifies valid attribute binding on PresentationProvides.'''
        provides: PresentationProvides = PresentationProvides(
            presenter=self.program_presenter,
            step_presenter=self.step_presenter,
        )
        self.assertIs(provides.presenter, self.program_presenter)
        self.assertIs(provides.step_presenter, self.step_presenter)

    def test_provides_immutability(self) -> None:
        '''Verifies PresentationProvides frozen dataclass raises error on mutation.'''
        provides: PresentationProvides = PresentationProvides(
            presenter=self.program_presenter,
            step_presenter=self.step_presenter,
        )
        with self.assertRaises(FrozenInstanceError):
            provides.presenter = self.program_presenter


if __name__ == '__main__':
    main()
