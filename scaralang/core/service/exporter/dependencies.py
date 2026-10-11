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
    Defines parameter dataclass ExporterDependencies for root exporter subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.exporter.csv.iexporter import ICsvExporter
from scaralang.core.service.exporter.gcode.iexporter import IGcodeExporter
from scaralang.core.service.exporter.json.iexporter import IJsonExporter
from scaralang.core.service.exporter.scara.iexporter import IScaraPlanExporter
from scaralang.core.service.exporter.svg.iexporter import ISvgExporter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.8'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ExporterDependencies:
    '''
        Bundle containing format exporter collaborators required by ScaraExporter.

        It defines:

            :attributes:
                | gcode_exporter - Injected IGcodeExporter protocol instance.
                | csv_exporter - Injected ICsvExporter protocol instance.
                | json_exporter - Injected IJsonExporter protocol instance.
                | svg_exporter - Injected ISvgExporter protocol instance.
                | scara_exporter - Injected IScaraPlanExporter protocol instance.
            :methods: None.
    '''

    gcode_exporter: IGcodeExporter
    csv_exporter: ICsvExporter
    json_exporter: IJsonExporter
    svg_exporter: ISvgExporter
    scara_exporter: IScaraPlanExporter
