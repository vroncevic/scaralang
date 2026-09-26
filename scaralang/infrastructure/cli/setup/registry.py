# -*- coding: UTF-8 -*-

'''
Module
    registry.py
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
    Registry for CLI bundle components.
'''

from __future__ import annotations

from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.utils.reflection import to_str

from scaralang.infrastructure.cli.setup.keys import CLIBundleKeys
from scaralang.infrastructure.cli.setup.dependencies import CLIBundleDependencies
from scaralang.infrastructure.cli.setup.dep_validator import CLIBundleDependenciesValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLIBundleRegistry:
    '''
        Registry for CLI bundle components.

        It defines:

            :attributes:
                | _dependencies - The registered dependencies of the CLI bundle.
            :methods:
                | __init__ - Initializes the registry with validated dependencies.
                | get - Retrieves a dependency by key.
                | __str__ - Returns the registry as string representation.
    '''

    _dependencies: CLIBundleDependencies

    def __init__(self, dependencies: CLIBundleDependencies) -> None:
        '''
            Initializes the registry with validated dependencies.

            :param dependencies: The CLI bundle dependencies.
            :exceptions:
                | ATSValueError: If dependencies are empty.
                | ATSTypeError:  If dependencies fail validation.
        '''
        CLIBundleDependenciesValidator.validate(dependencies)
        self._dependencies = dependencies

    def get(self, key: str) -> object:
        '''
            Retrieves a dependency by key.

            :param key: The key of the dependency.
            :return: The dependency object.
            :exceptions:
                | ATSValueError: If the key is not in registered dependencies.
        '''
        if key not in self._dependencies:
            raise ATSValueError(f'Key {key} not found in CLI bundle dependencies')
        return self._dependencies[key]  # type: ignore[literal-required]

    def __str__(self) -> str:
        '''
            Returns the registry as string representation.

            :return: The registry as string representation.
            :exceptions: None.
        '''
        return to_str(self)
