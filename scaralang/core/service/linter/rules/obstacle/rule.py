# -*- coding: UTF-8 -*-

'''
Module
    rule.py
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
    Implementation of ObstacleLintRule detecting trajectory collisions with keep-out zones.
'''

from __future__ import annotations

from typing import ClassVar

from scaralang.core.model.dsl.ast.command_type import ScaraCommandType
from scaralang.core.model.dsl.ast.instruction import ScaraInstruction
from scaralang.core.model.dsl.ast.instruction_param import ScaraInstructionParam
from scaralang.core.model.dsl.diagnostic.code import ScaraDiagnosticCode
from scaralang.core.model.dsl.diagnostic.diagnostic import ScaraDiagnostic
from scaralang.core.model.dsl.diagnostic.severity import ScaraDiagnosticSeverity
from scaralang.core.model.dsl.linter.context import LintContext
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.trajectory.obstacle.zone import ObstacleZone
from scaralang.core.service.linter.rules.obstacle.builder.ibuilder import IZoneBuilder
from scaralang.core.service.trajectory.avoidance.collision.ispatial_checker import ISpatialCollisionChecker
from scaralang.core.service.trajectory.avoidance.collision.izone_registry import IZoneRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ObstacleLintRule:
    '''
        Lint rule recording obstacle zones and detecting spatial path collisions.

        It defines:

            :cvar _MOTION_COMMANDS: Set of motion instruction types requiring collision checks.
            :attributes:
                | _zone_builder - Collaborator constructing ObstacleZone from ZONE_DEF.
                | _zone_registry - Collaborator managing registered obstacle zones.
                | _spatial_checker - Collaborator checking path collisions.
            :methods:
                | __init__ - Initializes ObstacleLintRule with injected collaborators.
                | name - Property returning rule identifier name.
                | check - Evaluates instruction against declared obstacle zones.
                | get_version - Gets implementation version string.
    '''

    _MOTION_COMMANDS: ClassVar[frozenset[ScaraCommandType]] = frozenset({
        ScaraCommandType.MOVE_L,
        ScaraCommandType.MOVE_J,
        ScaraCommandType.MOVE_REL,
        ScaraCommandType.JUMP,
        ScaraCommandType.APPROACH,
        ScaraCommandType.ARC_CW,
        ScaraCommandType.ARC_CCW,
        ScaraCommandType.RETRACT,
        ScaraCommandType.MOVE_PALLET,
    })

    def __init__(
        self,
        *,
        zone_builder: IZoneBuilder,
        zone_registry: IZoneRegistry,
        spatial_checker: ISpatialCollisionChecker,
    ) -> None:
        '''
            Initializes ObstacleLintRule with injected collaborators.

            :param zone_builder: Injected obstacle zone model builder.
            :param zone_registry: Injected obstacle zone registry.
            :param spatial_checker: Injected spatial collision detector.
        '''
        self._zone_builder: IZoneBuilder = zone_builder
        self._zone_registry: IZoneRegistry = zone_registry
        self._spatial_checker: ISpatialCollisionChecker = spatial_checker

    @property
    def name(self) -> str:
        '''
            Gets unique identifier name of the lint rule.

            :return: Rule identifier string.
        '''
        return 'obstacle'

    def check(
        self,
        *,
        instruction: ScaraInstruction,
        context: LintContext,
    ) -> tuple[ScaraDiagnostic, ...]:
        '''
            Evaluates instruction against obstacle zones, registering zones or emitting collision diagnostics.

            :param instruction: AST instruction node.
            :param context: Simulation lint context.
            :return: Tuple of detected diagnostic findings.
            :exceptions: None.
        '''
        if instruction.command_type == ScaraCommandType.ZONE_DEF:
            zone: ObstacleZone = self._zone_builder.build_zone(
                instruction=instruction
            )
            self._zone_registry.register_zone(zone)
            return ()

        if instruction.command_type in self._MOTION_COMMANDS:
            params: dict[str, object] = instruction.parameters
            x_key: str = ScaraInstructionParam.X.value
            y_key: str = ScaraInstructionParam.Y.value

            if x_key in params and y_key in params:
                val_x: object = params[x_key]
                val_y: object = params[y_key]
                if isinstance(val_x, (int, float)) and isinstance(val_y, (int, float)):
                    end_pt = Point2D(x=float(val_x), y=float(val_y))
                    zones: tuple[ObstacleZone, ...] = self._zone_registry.get_all_zones()
                    if zones:
                        if len(context.last_coords) >= 2:
                            start_pt = Point2D(
                                x=context.last_coords[0],
                                y=context.last_coords[1],
                            )
                            colliding = self._spatial_checker.is_segment_colliding(
                                start=start_pt, end=end_pt, zones=zones
                            )
                        else:
                            colliding = self._spatial_checker.is_point_colliding(
                                point=end_pt, zones=zones
                            )

                        if colliding:
                            return (
                                ScaraDiagnostic(
                                    code=ScaraDiagnosticCode.OBSTACLE_COLLISION.value,
                                    severity=ScaraDiagnosticSeverity.ERROR,
                                    message=(
                                        f'Trajectory collides with obstacle zone '
                                        f'{colliding[0].name}'
                                    ),
                                    line=instruction.line_number,
                                    command=instruction.command_type.value,
                                ),
                            )

        return ()

    def get_version(self) -> str:
        '''
            Gets implementation version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
