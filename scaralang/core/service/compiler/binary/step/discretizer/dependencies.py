# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle encapsulating inbound dependencies for StepDiscretizer.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.9'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class DiscretizerDependencies:
    '''
        Inbound parameter bundle for StepDiscretizer initialization.

        It defines:

            :attributes:
                | spatial - Injected ISpatialKinematicsSolver protocol instance.
                | transmission - Injected IJointStepTransmissionConverter protocol instance.
                | duration_calculator - Injected ISegmentDurationCalculator protocol instance.
    '''

    spatial: ISpatialKinematicsSolver
    transmission: IJointStepTransmissionConverter
    duration_calculator: ISegmentDurationCalculator
