# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Defines CLI class implementing inbound CLI port for scaralang.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from ats_utilities.option.imanager import IOptionManager
from ats_utilities.exceptions import ATSValueError, ATSTypeError
from ats_utilities.utils.reflection import to_str

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.infrastructure.cli.setup.bundle import CLIBundle
from scaralang.infrastructure.cli.setup.validator import CLIBundleValidator
from scaralang.infrastructure.command.icommand_definition import ICommandDefinition
from scaralang.infrastructure.command.icommand_executor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLI:
    '''
        Adapter that implements CLI commands for the scaralang toolchain.

        It defines:

            :attributes:
                | _service - SCARA DSL service.
                | _parser - Argument parser for parsing CLI command args.
                | _executors - Map of command names to command executor instances.
            :methods:
                | __init__ - Initializes the CLI with service, parser and commands list.
                | run - Parses command line arguments and runs selected command strategy.
                | is_initialized - Checks if the CLI is initialized.
                | __str__ - Returns the CLI as string representation.
    '''

    _service: IScaraDslService
    _parser: IOptionManager
    _executors: Mapping[str, ICommandExecutor[ICommandDefinition, object, object, object]]

    def __init__(self, bundle: CLIBundle) -> None:
        '''
            Initializes the CLI with service, parser and commands list.

            :param bundle: Bundle containing CLI adapters.
            :exceptions:
                | ATSValueError: If bundle fails validation.
                | ATSTypeError:  If bundle attributes have invalid types.
        '''
        CLIBundleValidator.validate(bundle)
        self._service: Final[IScaraDslService] = bundle.service
        self._parser: Final[IOptionManager] = bundle.parser
        self._executors: Final[
            Mapping[str, ICommandExecutor[ICommandDefinition, object, object, object]]
        ] = {pair.definition.name: pair.executor for pair in bundle.commands}
        self._parser.register_commands([pair.definition for pair in bundle.commands])

    def run(self) -> Mapping[str, object]:
        '''
            Parses command line arguments and runs selected command strategy.

            :return: The execution result (return code, stdout, and stderr).
            :exceptions: None.
        '''
        try:
            command_name, params = self._parser.parse_command()
            executor: (
                ICommandExecutor[ICommandDefinition, object, object, object] | None
            ) = self._executors.get(command_name)

            if executor is None:
                return {
                    'returncode': 1,
                    'stdout': '',
                    'stderr': f'cli::run - command {command_name} not found'
                }

            return executor.execute(params=params, service=self._service)

        except (ATSValueError, ATSTypeError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'cli::run - error: {exc}'}

        except (RuntimeError, OSError, ValueError, TypeError, KeyError) as exc:
            return {'returncode': 1, 'stdout': '', 'stderr': f'cli::run - unexpected error: {exc}'}

    def is_initialized(self) -> bool:
        '''
            Checks if the CLI adapter is initialized.

            :return: True if initialized, False otherwise.
            :exceptions: None.
        '''
        return bool(self._service and self._parser and self._executors)

    def __str__(self) -> str:
        '''
            Returns the CLI as string representation.

            :return: The CLI as string representation.
            :exceptions: None.
        '''
        return to_str(self)
