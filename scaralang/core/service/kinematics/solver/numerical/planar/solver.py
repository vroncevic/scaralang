# -*- coding: UTF-8 -*-

'''
Module
    solver.py
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
    Implementation of numerical planar Damped Least Squares (DLS) inverse kinematics solver.
'''

from __future__ import annotations

from math import pi, sqrt
from typing import ClassVar, Final

from scaralang.core.model.kinematics.solver.dls import DlsConfig
from scaralang.core.model.kinematics.solver.status import IkStatus
from scaralang.core.model.kinematics.solver.jacobian import JacobianMatrix2D
from scaralang.core.model.kinematics.pose.point_2d import Point2D
from scaralang.core.model.kinematics.solver.solution_2d import ScaraJoints2D
from scaralang.core.service.kinematics.solver.analytical.planar.isolver import IPlanarKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.jacobian.icalculator import IJacobianCalculator
from scaralang.core.service.kinematics.solver.numerical.planar.dependencies import NumericalPlanarDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.1.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class NumericalPlanarKinematicsSolver:
    '''
        Numerical planar inverse kinematics solver utilizing Damped Least Squares (DLS).

        It defines:

            :attributes:
                | _PI - Mathematical constant pi in radians.
                | _TWO_PI - Two pi full circle radians constant.
                | _jacobian_calc - Collaborator calculating differential Jacobian matrices.
                | _planar_solver - Collaborator computing forward kinematics.
                | _config - Injected DlsConfig parameters instance.
            :methods:
                | __init__ - Initializes solver with injected dependencies.
                | solve_dls_2d - Computes 2D joint angles via iterative DLS algorithm.
                | get_version - Returns solver component version string.
    '''

    _PI: ClassVar[float] = pi
    _TWO_PI: ClassVar[float] = 2.0 * pi

    _jacobian_calc: IJacobianCalculator
    _planar_solver: IPlanarKinematicsSolver
    _config: DlsConfig

    def __init__(
        self,
        dependencies: NumericalPlanarDependencies,
    ) -> None:
        '''
            Initializes numerical planar kinematics solver with injected dependencies.

            :param dependencies: Required NumericalPlanarDependencies bundle.
            :exceptions: None.
        '''
        self._jacobian_calc: Final[IJacobianCalculator] = dependencies.jacobian_calculator
        self._planar_solver: Final[IPlanarKinematicsSolver] = dependencies.planar_solver
        self._config: Final[DlsConfig] = dependencies.config

    def solve_dls_2d(
        self,
        target: Point2D,
        initial_angles: tuple[float, float],
    ) -> ScaraJoints2D:
        '''
            Solves 2D inverse kinematics using Damped Least Squares (DLS) iteration.

            :param target: Target Cartesian coordinate point in mm.
            :param initial_angles: Initial joint angles guess (theta1, theta2) in radians.
            :return: ScaraJoints2D result containing joint angles, reachability and status.
            :exceptions: None.
        '''
        cfg: DlsConfig = self._config
        th1, th2 = initial_angles
        converged: bool = False

        for _ in range(cfg.max_iterations):
            cur: Point2D = self._planar_solver.solve_fk_2d(th1, th2)
            dx: float = target.x - cur.x
            dy: float = target.y - cur.y

            if sqrt(dx * dx + dy * dy) <= cfg.tolerance_mm:
                converged = True
                break

            inv_j: JacobianMatrix2D = self._jacobian_calc.compute_damped_inverse(
                th1, th2, cfg.damping
            )
            dth1, dth2 = self._jacobian_calc.multiply_vector(inv_j, dx, dy)
            step: float = sqrt(dth1 * dth1 + dth2 * dth2)

            if step > cfg.step_limit_rad and step > 0.0:
                dth1 *= cfg.step_limit_rad / step
                dth2 *= cfg.step_limit_rad / step

            th1 += dth1
            th2 += dth2

        return ScaraJoints2D(
            theta1=(th1 + self._PI) % self._TWO_PI - self._PI,
            theta2=(th2 + self._PI) % self._TWO_PI - self._PI,
            reachable=converged,
            status=IkStatus.SUCCESS if converged else IkStatus.SINGULARITY,
        )

    def get_version(self) -> str:
        '''
            Returns solver component version string representation.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
