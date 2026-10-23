# -*- coding: UTF-8 -*-

'''
Module
    dls.py
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
    Defines DlsConfig immutable parameter model for Damped Least Squares numerical IK.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class DlsConfig:
    '''
        Configuration parameters controlling DLS numerical inverse kinematics solver.

        It defines:

            :attributes:
                | damping - Levenberg-Marquardt damping factor (lambda).
                | max_iterations - Maximum allowed Gauss-Newton iteration steps.
                | tolerance_mm - Position convergence threshold in mm.
                | step_limit_rad - Maximum angular step update per iteration in radians.
    '''

    damping: float = 0.05
    max_iterations: int = 50
    tolerance_mm: float = 0.01
    step_limit_rad: float = 0.2
