# -*- coding: UTF-8 -*-

'''
Module
    feedrate_validator_factory.py
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
    Factory instantiating and wiring FeedrateValidator component.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.service.trajectory.validation.feedrate.feedrate_validator import FeedrateValidator
from scaralang.core.service.trajectory.validation.feedrate.ifeedrate_validator import IFeedrateValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FeedrateValidatorFactory:
    '''
        Factory providing creation of FeedrateValidator instances.

        It defines:

            :methods:
                | create - Builds FeedrateValidator instance with injected bounds.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, bounds: ScaraBounds) -> IFeedrateValidator:
        '''
            Builds FeedrateValidator instance with injected bounds.

            :param bounds: Injected ScaraBounds instance.
            :return: IFeedrateValidator structural protocol instance.
            :exceptions: None.
        '''
        return FeedrateValidator(bounds=bounds)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
