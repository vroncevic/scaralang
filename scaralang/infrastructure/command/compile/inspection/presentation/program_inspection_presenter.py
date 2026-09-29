# -*- coding: UTF-8 -*-

'''
Module
    program_inspection_presenter.py
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
    Defines ProgramInspectionPresenter rendering comprehensive binary program inspection reports.
'''

from __future__ import annotations

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.infrastructure.command.compile.inspection.presentation.iframe_step_presenter import IFrameStepPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProgramInspectionPresenter:
    '''
        Renders full binary program inspection report with step cards and wire headers.

        It defines:

            :attributes:
                | _step_presenter - Injected step card presenter strategy.
            :methods:
                | __init__ - Initializes presenter with injected step presenter.
                | present_program - Generates formatted multi-line program inspection report.
    '''

    _step_presenter: IFrameStepPresenter

    def __init__(self, *, step_presenter: IFrameStepPresenter) -> None:
        '''
            Initializes ProgramInspectionPresenter with injected step presenter.

            :param step_presenter: Step card presenter strategy.
        '''
        self._step_presenter = step_presenter

    def present_program(self, *, program: BinaryProgram) -> str:
        '''
            Renders complete frame inspection report for a compiled binary program.

            :param program: Compiled BinaryProgram containing steps and raw bytes.
            :return: Formatted multi-line inspection report.
        '''
        border: str = '=' * 80
        sep: str = '-' * 80
        banner: str = (
            f'{border}\n'
            f'SCARA BINARY FRAME INSPECTION: {len(program.steps)} Frames Compiled '
            f'({len(program.raw_bytes)} bytes total)\n'
            f'{border}'
        )

        if not program.steps:
            return f'{banner}\n(No frames compiled)\n{border}'

        step_cards: list[str] = [
            self._step_presenter.present_step(step=step, index=idx)
            for idx, step in enumerate(program.steps, start=1)
        ]
        body: str = f'\n{sep}\n'.join(step_cards)
        return f'{banner}\n{body}\n{border}'
