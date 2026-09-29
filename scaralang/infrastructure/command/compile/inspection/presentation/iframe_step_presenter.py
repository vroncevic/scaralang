# -*- coding: UTF-8 -*-

'''
Module
    iframe_step_presenter.py
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
    Defines structural interface protocol for presenting individual binary motion steps.
'''

from __future__ import annotations

from typing import Protocol
from typing import runtime_checkable

from scaralang.core.model.dsl.binary.step import Step

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IFrameStepPresenter(Protocol):
    '''
        Structural interface protocol for rendering visual inspection cards for binary steps.

        It defines:

            :methods:
                | present_step - Formats a Step into multi-line wire inspection card.
    '''

    def present_step(self, *, step: Step, index: int) -> str:
        '''
            Renders complete visual card for a single compiled Step.

            :param step: Step entity to render.
            :param index: 1-based sequential step index.
            :return: Multi-line formatted card string.
        '''
