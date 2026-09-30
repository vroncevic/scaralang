# -*- coding: UTF-8 -*-

'''
Module
    scara_dsl_service_test.py
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
    Unit tests for ScaraDslService facade operations.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.ast.program import ScaraProgram
from scaralang.core.model.dsl.binary.disassembled_frame import DisassembledFrame
from scaralang.core.model.dsl.binary.disassembly_summary import DisassemblySummary
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.dsl.scara_dsl_bundle import ScaraDslBundle
from scaralang.core.service.dsl.scara_dsl_service import ScaraDslService
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scaralang.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scaralang'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scaralang/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraDslService(TestCase):
    '''
        Test cases verifying ScaraDslService facade operations.

        It defines:

            :methods:
                | setUp - Initializes test fixtures using default factory.
                | test_is_initialized - Verifies initialization health check.
                | test_compile_script_success - Verifies compiling valid SCARA script.
                | test_compile_program_success - Verifies compiling AST program.
                | test_validate_script - Verifies script validation returning diagnostics.
                | test_export_plan - Verifies round-trip plan export to SCARA DSL code.
                | test_compile_plan - Verifies compiling trajectory plan to binary.
                | test_compile_to_binary - Verifies script compilation directly to binary.
                | test_compile_to_bytes - Verifies script compilation directly to bytes.
                | test_disassemble_bytes - Verifies binary disassembly through facade.
                | test_get_toolchain_info - Verifies retrieving toolchain metadata.
                | test_compile_pick_and_place - Verifies pick and place compilation.
                | test_lint_script - Verifies diagnostic reporting through lint_script facade.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures using default factory.
        '''
        self.service = ScaraDslServiceFactory.create_default(
            frame_builder=BinaryFrameBuilderFactory.create(),
            frame_parser=BinaryFrameParserFactory.create_default(),
            payload_unpacker=BinaryPayloadUnpacker(),
        )

    def test_is_initialized(self) -> None:
        '''
            Verifies is_initialized returns True when all subcomponents exist.
        '''
        self.assertTrue(self.service.is_initialized())

    def test_compile_script_success(self) -> None:
        '''
            Verifies compiling valid SCARA script into populated TrajectoryPlan.
        '''
        code = (
            'CONFIG ELBOW RIGHT\n'
            'SPEED RAPID 100.0\n'
            'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
            'MOVE_L X=160.0 Y=60.0 Z=20.0 SPEED=40.0\n'
        )
        plan = self.service.compile_script(source=code)
        self.assertGreaterEqual(plan.count, 2)
        first_pt = plan.waypoints[0]
        self.assertAlmostEqual(first_pt.x, 150.0)
        self.assertAlmostEqual(first_pt.y, 50.0)

    def test_compile_program_success(self) -> None:
        '''
            Verifies compile_program delegates to injected compiler.
        '''
        mock_compiler = MagicMock()
        mock_plan = MagicMock()
        mock_compiler.compile_program.return_value = mock_plan
        bundle = ScaraDslBundle(
            compiler=mock_compiler,
            validator=MagicMock(),
            exporter=MagicMock(),
            binary_service=MagicMock(),
            toolchain_info=MagicMock(),
        )
        service = ScaraDslService(bundle=bundle)
        program = ScaraProgram(instructions=())
        plan = service.compile_program(program=program)
        self.assertEqual(plan, mock_plan)
        mock_compiler.compile_program.assert_called_once_with(program=program)

    def test_validate_script(self) -> None:
        '''
            Verifies validation diagnostics for valid and invalid scripts.
        '''
        valid_code = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        is_valid, msgs = self.service.validate_script(source=valid_code)
        self.assertTrue(is_valid)
        self.assertTrue(any('PASSED' in m for m in msgs))

        invalid_code = 'MOVE_J X=9999.0 Y=9999.0 Z=20.0\n'
        is_valid_inv, msgs_inv = self.service.validate_script(source=invalid_code)
        self.assertFalse(is_valid_inv)
        self.assertTrue(len(msgs_inv) > 0)

    def test_export_plan(self) -> None:
        '''
            Verifies exporting a TrajectoryPlan into SCARA DSL source text.
        '''
        plan = TrajectoryPlanFactory.create()
        plan.add_point(
            Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=30.0, name='P1', command='')
        )
        plan.add_point(
            Waypoint(x=180.0, y=60.0, z=10.0, phi=15.0, speed=40.0, name='P2', command='')
        )

        exported = self.service.export_plan(plan=plan)
        self.assertIn('MOVE_J X=150.00 Y=50.00', exported)
        self.assertIn('MOVE_L X=180.00 Y=60.00', exported)
        self.assertIn('# P1', exported)
        self.assertIn('# P2', exported)

    def test_compile_plan(self) -> None:
        '''
            Verifies compile_plan produces BinaryProgram package.
        '''
        plan = TrajectoryPlanFactory.create()
        plan.add_point(
            Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=30.0, name='P1', command='')
        )
        prog = self.service.compile_plan(plan=plan)
        self.assertIsInstance(prog, BinaryProgram)

    def test_compile_to_binary(self) -> None:
        '''
            Verifies compile_to_binary returns BinaryProgram.
        '''
        code = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        prog = self.service.compile_to_binary(source=code)
        self.assertIsInstance(prog, BinaryProgram)
        self.assertTrue(len(prog.raw_bytes) > 0)

    def test_compile_to_bytes(self) -> None:
        '''
            Verifies compile_to_bytes returns wire bytes directly.
        '''
        code = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        raw = self.service.compile_to_bytes(source=code)
        self.assertIsInstance(raw, bytes)
        self.assertTrue(len(raw) > 0)

    def test_disassemble_bytes(self) -> None:
        '''
            Verifies disassemble_bytes processes wire bytes into frame models.
        '''
        code = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        raw = self.service.compile_to_bytes(source=code)
        frames = self.service.disassemble_bytes(data=raw)
        self.assertIsInstance(frames, tuple)
        self.assertTrue(len(frames) > 0)
        self.assertIsInstance(frames[0], DisassembledFrame)

    def test_get_toolchain_info(self) -> None:
        '''
            Verifies get_toolchain_info returns metadata specification.
        '''
        info = self.service.get_toolchain_info(verbose=True)
        self.assertIsInstance(info, tuple)
        self.assertTrue(any('scaralang: SCARA' in line for line in info))

    def test_compile_pick_and_place(self) -> None:
        '''
            Verifies compiling a pick and place script containing tool and wait instructions.
        '''
        code = (
            'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
            'WAIT 200\n'
            'PUMP ON\n'
            'MOVE_L X=160.0 Y=60.0 Z=10.0\n'
            'PUMP OFF\n'
            'VALVE ON\n'
            'WAIT 100\n'
            'VALVE OFF\n'
        )
        plan = self.service.compile_script(source=code)
        commands = [pt.command for pt in plan.waypoints if pt.command]
        self.assertIn('<CMD:WAIT#200>', commands)
        self.assertIn('<CMD:PUMP#1>', commands)
        self.assertIn('<CMD:PUMP#0>', commands)
        self.assertIn('<CMD:VALVE#1>', commands)
        self.assertIn('<CMD:VALVE#0>', commands)
        self.assertIn('<CMD:WAIT#100>', commands)

    def test_lint_script(self) -> None:
        '''
            Verifies diagnostic reporting through lint_script facade.
        '''
        code = (
            'HOME\n'
            'PUMP ON\n'
            'PUMP ON\n'
        )
        diagnostics = self.service.lint_script(source=code)
        self.assertTrue(any(d.code == 'REDUNDANT_TOOL_CMD' for d in diagnostics))

    def test_calculate_disassembly_summary(self) -> None:
        '''
            Verifies calculate_disassembly_summary returns DisassemblySummary domain model.
        '''
        code = 'HOME\nMOVE_J X=100.0 Y=100.0 Z=10.0\nWAIT 200\nPUMP ON\n'
        raw = self.service.compile_to_bytes(source=code)
        frames = self.service.disassemble_bytes(data=raw)
        summary = self.service.calculate_disassembly_summary(
            frames=frames, byte_count=len(raw)
        )
        self.assertIsInstance(summary, DisassemblySummary)
        self.assertEqual(summary.total_bytes, len(raw))
        self.assertEqual(summary.decoded_frames, len(frames))
        self.assertGreater(summary.motion_frames, 0)
        self.assertGreater(summary.tool_commands, 0)
        self.assertGreater(summary.wait_delays, 0)
        self.assertGreater(summary.system_frames, 0)

    def test_compile_and_disassemble_motor_config(self) -> None:
        '''
            Verifies end-to-end round-trip of CONFIG MOTOR command through compiler and disassembler.
        '''
        code = 'CONFIG MOTOR CLOSED_LOOP\nMOVE_J X=150.0 Y=50.0 Z=20.0\n'
        raw = self.service.compile_to_bytes(source=code)
        self.assertIsInstance(raw, bytes)
        self.assertTrue(len(raw) > 0)
        frames = self.service.disassemble_bytes(data=raw)
        self.assertGreaterEqual(len(frames), 2)
        self.assertEqual(frames[0].msg_id, 0x0F)
        self.assertEqual(frames[0].msg_name, 'CMD_CONFIG_MOTOR')
        self.assertEqual(frames[0].detail, 'CONFIG MOTOR CLOSED_LOOP')

    def test_lint_motor_config(self) -> None:
        '''
            Verifies linter diagnostic reporting for motor configuration commands.
        '''
        code = (
            'HOME\n'
            'CONFIG MOTOR OPEN_LOOP\n'
            'CONFIG MOTOR OPEN_LOOP\n'
        )
        diagnostics = self.service.lint_script(source=code)
        self.assertTrue(any(d.code == 'REDUNDANT_MOTOR_CONFIG' for d in diagnostics))


if __name__ == '__main__':
    main()
