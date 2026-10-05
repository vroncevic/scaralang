# -*- coding: UTF-8 -*-

'''
Module
    csv_trajectory_exporter_factory.py
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
    Factory instantiating CsvTrajectoryExporter instances.
'''

from __future__ import annotations

from scaralang.core.service.exporter.csv.csv_trajectory_exporter import CsvTrajectoryExporter
from scaralang.core.service.exporter.csv.icsv_trajectory_exporter import ICsvTrajectoryExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CsvTrajectoryExporterFactory:
    '''
        Factory providing ICsvTrajectoryExporter instances.

        It defines:

            :methods:
                | create - Builds CsvTrajectoryExporter instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ICsvTrajectoryExporter:
        '''
            Builds and returns an ICsvTrajectoryExporter protocol instance.

            :return: Fully wired ICsvTrajectoryExporter protocol instance.
            :exceptions: None.
        '''
        return CsvTrajectoryExporter()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
