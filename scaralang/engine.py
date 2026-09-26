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
    Engine orchestrating the initialization and execution of scaralang.
'''

from __future__ import annotations

from collections.abc import Mapping
from logging import INFO, ERROR
from sys import stdout

from ats_utilities.base.engine import Base
from ats_utilities.logger.ilogger import ILogger
from ats_utilities.exceptions import ATSValueError, ATSTypeError

from scaralang.setup.bundle import ScaralangBundle
from scaralang.setup.validator import ScaralangBundleValidator
from scaralang.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Scaralang(Base):
    '''
        Engine orchestrating the initialization and execution of scaralang.

        It defines:

            :attributes:
                | _is_initialized - Flag indicating whether the engine is initialized.
                | _logger - The logger for logging messages during execution.
                | _cli - The adapter for the command line interface.
            :methods:
                | __init__ - Initializes the engine with adapters and services.
                | process - Processes the scaralang CLI commands.
    '''

    _is_initialized: bool
    _logger: ILogger | None
    _cli: ICLI

    def __init__(self, bundle: ScaralangBundle) -> None:
        '''
            Initializes the scaralang engine with adapters and services.

            :param bundle: Scaralang bundle containing adapters and services.
            :exceptions: None.
        '''
        self._is_initialized = False
        self._logger = None

        try:
            ScaralangBundleValidator.validate(bundle)
            super().__init__(bundle.base)

            self._cli = bundle.cli
            self._is_initialized = all(
                component.is_initialized() for component in [
                    bundle.base.option_manager,
                    bundle.service,
                    self._cli
                ] if component
            )

            self._logger = self.get_context().logger
            self._logger.write_log(INFO, '✅ scaralang: engine initialized successfully!')

        except (ATSValueError, ATSTypeError) as exc:
            stdout.write(f'❌ scaralang: {exc}!\n')

        except Exception as exc:
            stdout.write(f'❌ scaralang unexpected exception: {exc}!\n')

    def process(self, verbose: bool = False) -> bool:
        '''
            Processes the scaralang commands.

            :param verbose: Enable verbose output.
            :return: True if successful, False otherwise.
            :exceptions: None.
        '''
        result: Mapping[str, object] = {}

        try:
            if self.is_initialized() and self._logger is not None:
                self._logger.write_log(INFO, '🔥 Starting execution command...')
                result = self._cli.run()
                self._logger.write_log(INFO, '✅ Execution finished!')

                stdout_text = str(result.get('stdout') or '')
                if stdout_text:
                    stdout.write(f'{stdout_text}\n')

                if result.get('returncode') != 0:
                    err_msg = str(result.get('stderr') or 'failed!')
                    self._logger.write_log(ERROR, f'❌ scaralang: {err_msg}')
                    stdout.write(f'❌ scaralang: {err_msg}\n')
                    return False

                self._logger.write_log(INFO, '✅ scaralang: done!')
                return True

            if self._logger is not None:
                self._logger.write_log(ERROR, '❌ scaralang: engine not initialized!')
            else:
                stdout.write('❌ scaralang: engine not initialized!\n')
            return False

        except (ATSValueError, ATSTypeError) as exc:
            if self._logger is not None:
                self._logger.write_log(ERROR, f'❌ scaralang: {exc}!')
            else:
                stdout.write(f'❌ scaralang: {exc}!\n')
            return False

        except Exception as exc:
            if self._logger is not None:
                self._logger.write_log(ERROR, f'❌ scaralang unexpected exception: {exc}!')
            else:
                stdout.write(f'❌ scaralang unexpected exception: {exc}!\n')
            return False
