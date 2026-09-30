.. image:: _static/scaralang_logo.png
   :align: right
   :width: 25%

SCARA Robotics Domain-Specific Language (DSL) Toolchain & Binary Protocol Codec
===============================================================================

**scaralang** is a standalone, lightweight, GUI-independent Python toolchain and compiler for the **SCARA Robotics Domain-Specific Language (DSL)**, combined with the official **SCARA Wire Binary Protocol Codec**.

Developed in `python <https://www.python.org/>`_ code.

The README is used to introduce the tool and provide instructions on
how to install the tool, any machine dependencies it may have and any
other information that should be provided before the tool is installed.

|scaralang python checker| |scaralang python package| |scaralang interface checker| |scaralang isp checker| |scaralang srp checker| |gplv3 license| |apache license| |python version| |github issues| |documentation status| |github contributors|

.. |scaralang python checker| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python_checker.yml

.. |scaralang python package| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_package_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_package_checker.yml

.. |scaralang interface checker| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_interface_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_interface_checker.yml

.. |scaralang isp checker| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_isp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_isp_checker.yml

.. |scaralang srp checker| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_srp_checker.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_srp_checker.yml

.. |gplv3 license| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |apache license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

.. |python version| image:: https://img.shields.io/badge/python-3.10+-blue.svg
   :target: https://www.python.org/downloads/

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/scaralang.svg
   :target: https://github.com/vroncevic/scaralang/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/scaralang.svg
   :target: https://github.com/vroncevic/scaralang/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/scaralang/badge/?version=latest
   :target: https://scaralang.readthedocs.io/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents

   self
   modules

🚀 Installation
--------------------------------------------------------------------------------

|scaralang python3 build|

.. |scaralang python3 build| image:: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python3_build.yml/badge.svg
   :target: https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python3_build.yml

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/scaralang/releases

To install **scaralang** type the following

.. code-block:: bash

    tar xvzf scaralang-x.y.z.tar.gz
    cd scaralang-x.y.z/
    # python3
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py 
    python3 -m pip install --upgrade setuptools
    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade build
    pip3 install -r requirements.txt
    python3 -m build --no-isolation --wheel
    pip3 install ./dist/scaralang-*-py3-none-any.whl
    rm -f get-pip.py

You can use Docker to create image/container, or You can use pip to install

.. code-block:: bash

    # python3
    pip3 install scaralang

📦 Dependencies
--------------------------------------------------------------------------------

**scaralang** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_ |ats gplv3| |ats apache|

.. |ats gplv3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |ats apache| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

📁 Tool structure
--------------------------------------------------------------------------------

**scaralang** is based on OOP and Clean Architecture.

Tool structure

.. code-block:: bash

    scaralang/
         ├── core/
         │   ├── __init__.py
         │   ├── model/
         │   │   ├── dsl/
         │   │   │   ├── ast/
         │   │   │   │   ├── command_type.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── instruction.py
         │   │   │   │   ├── instruction_param.py
         │   │   │   │   ├── jog_axis.py
         │   │   │   │   ├── pneumatic_state.py
         │   │   │   │   ├── program.py
         │   │   │   │   ├── speed_mode.py
         │   │   │   │   ├── tool_orient_mode.py
         │   │   │   │   ├── tool_position.py
         │   │   │   │   └── zone_mode.py
         │   │   │   ├── binary/
         │   │   │   │   ├── binary_program_telemetry.py
         │   │   │   │   ├── disassembled_frame.py
         │   │   │   │   ├── disassembly_summary.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── parsed_command_token.py
         │   │   │   │   ├── program.py
         │   │   │   │   └── step.py
         │   │   │   ├── compiler/
         │   │   │   │   ├── arc_geometry.py
         │   │   │   │   ├── control_waypoint_descriptor.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── scara_compiler_context.py
         │   │   │   ├── diagnostic/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── scara_diagnostic.py
         │   │   │   │   ├── scara_diagnostic_code.py
         │   │   │   │   └── scara_diagnostic_severity.py
         │   │   │   ├── exporter/
         │   │   │   │   ├── export_format.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── __init__.py
         │   │   │   ├── linter/
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── scara_lint_context.py
         │   │   │   ├── macro/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── pallet_definition.py
         │   │   │   │   └── work_frame.py
         │   │   │   └── token/
         │   │   │       ├── __init__.py
         │   │   │       ├── lexer_pattern_kind.py
         │   │   │       ├── scara_token.py
         │   │   │       └── scara_token_type.py
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── elbow_config.py
         │   │   │   ├── __init__.py
         │   │   │   ├── point_2d.py
         │   │   │   ├── point_3d.py
         │   │   │   ├── scara_bounds.py
         │   │   │   └── transmission_parameters.py
         │   │   ├── motor/
         │   │   │   ├── axis_mask.py
         │   │   │   ├── __init__.py
         │   │   │   ├── motor_config.py
         │   │   │   ├── motor_drive_mode.py
         │   │   │   └── motor_interface_type.py
         │   │   ├── protocol/
         │   │   │   ├── binary_delimiter.py
         │   │   │   ├── binary_frame.py
         │   │   │   ├── error_code.py
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_steps.py
         │   │   │   ├── message_id.py
         │   │   │   ├── motor_wire_mode.py
         │   │   │   └── tool_id.py
         │   │   ├── repl/
         │   │   │   ├── __init__.py
         │   │   │   ├── repl_dispatch_result.py
         │   │   │   └── repl_session_context.py
         │   │   └── trajectory/
         │   │       ├── arc_point.py
         │   │       ├── axis_peak_metric.py
         │   │       ├── bottleneck_incident.py
         │   │       ├── circle_geometry.py
         │   │       ├── __init__.py
         │   │       ├── trajectory_cycle_report.py
         │   │       ├── validation_result.py
         │   │       └── waypoint.py
         │   └── service/
         │       ├── compiler/
         │       │   ├── binary/
         │       │   │   ├── binary_compiler.py
         │       │   │   ├── binary_compiler_factory.py
         │       │   │   ├── command/
         │       │   │   │   ├── command_compiler.py
         │       │   │   │   ├── command_compiler_factory.py
         │       │   │   │   ├── icommand_compiler.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motor/
         │       │   │   │   │   ├── imotor_frame_builder.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── motor_frame_builder.py
         │       │   │   │   │   └── motor_frame_builder_factory.py
         │       │   │   │   ├── tokens/
         │       │   │   │   │   ├── command_token_parser.py
         │       │   │   │   │   ├── command_token_parser_factory.py
         │       │   │   │   │   ├── icommand_token_parser.py
         │       │   │   │   │   └── __init__.py
         │       │   │   │   └── tool/
         │       │   │   │       ├── __init__.py
         │       │   │   │       ├── itool_frame_builder.py
         │       │   │   │       ├── tool_frame_builder.py
         │       │   │   │       └── tool_frame_builder_factory.py
         │       │   │   ├── ibinary_compiler.py
         │       │   │   ├── __init__.py
         │       │   │   ├── metrics/
         │       │   │   │   ├── binary_metrics_calculator.py
         │       │   │   │   ├── binary_metrics_calculator_factory.py
         │       │   │   │   ├── ibinary_metrics_calculator.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── motion/
         │       │   │   │   ├── imotion_compiler.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motion_compiler.py
         │       │   │   │   └── motion_compiler_factory.py
         │       │   │   └── step/
         │       │   │       ├── __init__.py
         │       │   │       ├── istep_discretizer.py
         │       │   │       ├── iwaypoint_step_dispatcher.py
         │       │   │       ├── step_discretizer.py
         │       │   │       ├── step_discretizer_factory.py
         │       │   │       ├── waypoint_step_dispatcher.py
         │       │   │       └── waypoint_step_dispatcher_factory.py
         │       │   ├── frame/
         │       │   │   ├── frame_transformer.py
         │       │   │   ├── frame_transformer_factory.py
         │       │   │   ├── iframe_transformer.py
         │       │   │   └── __init__.py
         │       │   ├── iinstruction_pipeline.py
         │       │   ├── __init__.py
         │       │   ├── instruction_pipeline.py
         │       │   ├── instruction_pipeline_factory.py
         │       │   ├── iprimitive_instruction_processor.py
         │       │   ├── iscara_compiler.py
         │       │   ├── macro/
         │       │   │   ├── frame_macro_expander.py
         │       │   │   ├── frame_macro_expander_factory.py
         │       │   │   ├── imacro_expander.py
         │       │   │   ├── __init__.py
         │       │   │   ├── itangent_macro_expander.py
         │       │   │   ├── jump_macro_expander.py
         │       │   │   ├── jump_macro_expander_factory.py
         │       │   │   ├── pallet_macro_expander.py
         │       │   │   ├── pallet_macro_expander_factory.py
         │       │   │   ├── tangent_macro_expander.py
         │       │   │   └── tangent_macro_expander_factory.py
         │       │   ├── motion/
         │       │   │   ├── arc/
         │       │   │   │   ├── arc_move_compiler.py
         │       │   │   │   ├── arc_move_compiler_factory.py
         │       │   │   │   ├── builder/
         │       │   │   │   │   ├── arc_waypoint_builder.py
         │       │   │   │   │   ├── arc_waypoint_builder_factory.py
         │       │   │   │   │   ├── iarc_waypoint_builder.py
         │       │   │   │   │   └── __init__.py
         │       │   │   │   ├── calculator/
         │       │   │   │   │   ├── arc_point_calculator.py
         │       │   │   │   │   ├── arc_point_calculator_factory.py
         │       │   │   │   │   ├── iarc_point_calculator.py
         │       │   │   │   │   └── __init__.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── interpolation/
         │       │   │   │       ├── arc_interpolator.py
         │       │   │   │       ├── arc_interpolator_factory.py
         │       │   │   │       ├── iarc_interpolator.py
         │       │   │   │       └── __init__.py
         │       │   │   ├── cartesian/
         │       │   │   │   ├── cartesian_move_compiler.py
         │       │   │   │   ├── cartesian_move_compiler_factory.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── imotion_sub_compiler.py
         │       │   │   ├── __init__.py
         │       │   │   ├── motion_command_compiler.py
         │       │   │   ├── motion_command_compiler_factory.py
         │       │   │   └── vertical/
         │       │   │       ├── __init__.py
         │       │   │       ├── vertical_move_compiler.py
         │       │   │       └── vertical_move_compiler_factory.py
         │       │   ├── primitive/
         │       │   │   ├── control/
         │       │   │   │   ├── control_command_compiler.py
         │       │   │   │   ├── control_command_compiler_factory.py
         │       │   │   │   ├── control_waypoint_builder.py
         │       │   │   │   ├── control_waypoint_builder_factory.py
         │       │   │   │   ├── icontrol_waypoint_builder.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iprimitive_compiler.py
         │       │   │   ├── state/
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── state_command_compiler.py
         │       │   │   │   └── state_command_compiler_factory.py
         │       │   │   └── tool/
         │       │   │       ├── __init__.py
         │       │   │       ├── itool_waypoint_builder.py
         │       │   │       ├── tool_command_compiler.py
         │       │   │       ├── tool_command_compiler_factory.py
         │       │   │       ├── tool_waypoint_builder.py
         │       │   │       └── tool_waypoint_builder_factory.py
         │       │   ├── primitive_instruction_processor.py
         │       │   ├── primitive_instruction_processor_factory.py
         │       │   ├── scara_compiler.py
         │       │   └── scara_compiler_factory.py
         │       ├── disassembler/
         │       │   ├── frame_detail_decoder.py
         │       │   ├── frame_detail_decoder_factory.py
         │       │   ├── iframe_detail_decoder.py
         │       │   ├── __init__.py
         │       │   ├── iscara_disassembler.py
         │       │   ├── scara_disassembler.py
         │       │   └── scara_disassembler_factory.py
         │       ├── dsl/
         │       │   ├── binary/
         │       │   │   ├── binary_service.py
         │       │   │   ├── binary_service_factory.py
         │       │   │   ├── ibinary_service.py
         │       │   │   └── __init__.py
         │       │   ├── compilation/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_dsl_compiler.py
         │       │   │   ├── scara_dsl_compiler.py
         │       │   │   └── scara_dsl_compiler_factory.py
         │       │   ├── __init__.py
         │       │   ├── iscara_dsl_binary_compiler.py
         │       │   ├── iscara_dsl_disassembler.py
         │       │   ├── iscara_dsl_info_provider.py
         │       │   ├── iscara_dsl_linter.py
         │       │   ├── iscara_dsl_service.py
         │       │   ├── iscara_dsl_validator.py
         │       │   ├── scara_dsl_bundle.py
         │       │   ├── scara_dsl_pipeline_bundle.py
         │       │   ├── scara_dsl_service.py
         │       │   ├── scara_dsl_service_factory.py
         │       │   ├── toolchain/
         │       │   │   ├── __init__.py
         │       │   │   ├── itoolchain_info_provider.py
         │       │   │   ├── toolchain_info_provider.py
         │       │   │   └── toolchain_info_provider_factory.py
         │       │   └── validation/
         │       │       ├── __init__.py
         │       │       ├── scara_script_validator.py
         │       │       └── scara_script_validator_factory.py
         │       ├── exporter/
         │       │   ├── csv/
         │       │   │   ├── csv_trajectory_exporter.py
         │       │   │   ├── csv_trajectory_exporter_factory.py
         │       │   │   ├── icsv_trajectory_exporter.py
         │       │   │   └── __init__.py
         │       │   ├── export_dispatcher_bundle.py
         │       │   ├── export_target_dispatcher.py
         │       │   ├── export_target_dispatcher_factory.py
         │       │   ├── gcode/
         │       │   │   ├── gcode_exporter.py
         │       │   │   ├── gcode_exporter_factory.py
         │       │   │   ├── igcode_exporter.py
         │       │   │   └── __init__.py
         │       │   ├── iexport_target_dispatcher.py
         │       │   ├── __init__.py
         │       │   ├── json/
         │       │   │   ├── ijson_trajectory_exporter.py
         │       │   │   ├── __init__.py
         │       │   │   ├── json_trajectory_exporter.py
         │       │   │   └── json_trajectory_exporter_factory.py
         │       │   ├── scara/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_plan_exporter.py
         │       │   │   ├── scara_plan_exporter.py
         │       │   │   ├── scara_plan_exporter_factory.py
         │       │   │   ├── scara_program_serializer.py
         │       │   │   └── scara_source_generator.py
         │       │   └── svg/
         │       │       ├── __init__.py
         │       │       ├── isvg_trajectory_exporter.py
         │       │       ├── svg_trajectory_exporter.py
         │       │       └── svg_trajectory_exporter_factory.py
         │       ├── __init__.py
         │       ├── kinematics/
         │       │   ├── default_scara_profile.py
         │       │   ├── ikinematics_service.py
         │       │   ├── __init__.py
         │       │   ├── kinematics_service.py
         │       │   ├── kinematics_service_factory.py
         │       │   └── transmission/
         │       │       ├── ijoint_step_transmission_converter.py
         │       │       ├── __init__.py
         │       │       ├── joint_step_transmission_converter.py
         │       │       └── joint_step_transmission_converter_factory.py
         │       ├── linter/
         │       │   ├── diagnostic/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_diagnostic_formatter.py
         │       │   │   ├── scara_diagnostic_formatter.py
         │       │   │   └── scara_diagnostic_formatter_factory.py
         │       │   ├── __init__.py
         │       │   ├── iscara_linter.py
         │       │   ├── rules/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_lint_rule.py
         │       │   │   ├── motion/
         │       │   │   │   ├── imotion_calibration_validator.py
         │       │   │   │   ├── imotion_duplicate_validator.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motion_calibration_validator.py
         │       │   │   │   ├── motion_calibration_validator_factory.py
         │       │   │   │   ├── motion_duplicate_validator.py
         │       │   │   │   ├── motion_duplicate_validator_factory.py
         │       │   │   │   ├── motion_lint_rule.py
         │       │   │   │   └── motion_lint_rule_factory.py
         │       │   │   ├── pneumatic/
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── ipneumatic_conflict_validator.py
         │       │   │   │   ├── ipneumatic_flyby_validator.py
         │       │   │   │   ├── ipneumatic_redundancy_validator.py
         │       │   │   │   ├── pneumatic_conflict_validator.py
         │       │   │   │   ├── pneumatic_conflict_validator_factory.py
         │       │   │   │   ├── pneumatic_flyby_validator.py
         │       │   │   │   ├── pneumatic_flyby_validator_factory.py
         │       │   │   │   ├── pneumatic_lint_rule.py
         │       │   │   │   ├── pneumatic_lint_rule_factory.py
         │       │   │   │   ├── pneumatic_redundancy_validator.py
         │       │   │   │   └── pneumatic_redundancy_validator_factory.py
         │       │   │   ├── state/
         │       │   │   │   ├── imotor_mode_validator.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── istate_homing_validator.py
         │       │   │   │   ├── istate_zone_validator.py
         │       │   │   │   ├── motor_mode_validator.py
         │       │   │   │   ├── motor_mode_validator_factory.py
         │       │   │   │   ├── state_homing_validator.py
         │       │   │   │   ├── state_homing_validator_factory.py
         │       │   │   │   ├── state_lint_rule.py
         │       │   │   │   ├── state_lint_rule_factory.py
         │       │   │   │   ├── state_zone_validator.py
         │       │   │   │   └── state_zone_validator_factory.py
         │       │   │   └── timing/
         │       │   │       ├── __init__.py
         │       │   │       ├── itiming_blend_zone_validator.py
         │       │   │       ├── itiming_dwell_validator.py
         │       │   │       ├── timing_blend_zone_validator.py
         │       │   │       ├── timing_blend_zone_validator_factory.py
         │       │   │       ├── timing_dwell_validator.py
         │       │   │       ├── timing_dwell_validator_factory.py
         │       │   │       ├── timing_lint_rule.py
         │       │   │       └── timing_lint_rule_factory.py
         │       │   ├── scara_linter.py
         │       │   └── scara_linter_factory.py
         │       ├── motor/
         │       │   ├── __init__.py
         │       │   ├── motor_config_factory.py
         │       │   ├── motor_drive_mode_resolver.py
         │       │   ├── motor_interface_resolver.py
         │       │   └── motor_wire_mode_converter.py
         │       ├── parser/
         │       │   ├── commands/
         │       │   │   ├── config/
         │       │   │   │   ├── accel_config_parser.py
         │       │   │   │   ├── config_command_parser_factory.py
         │       │   │   │   ├── elbow_config_parser.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motor_config_parser.py
         │       │   │   │   ├── override_config_parser.py
         │       │   │   │   ├── speed_config_parser.py
         │       │   │   │   ├── tool_orient_command_parser.py
         │       │   │   │   └── zone_command_parser.py
         │       │   │   ├── flow/
         │       │   │   │   ├── disable_command_parser.py
         │       │   │   │   ├── enable_command_parser.py
         │       │   │   │   ├── estop_command_parser.py
         │       │   │   │   ├── flow_command_parser_factory.py
         │       │   │   │   ├── hold_command_parser.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── resume_command_parser.py
         │       │   │   │   ├── sync_command_parser.py
         │       │   │   │   └── wait_command_parser.py
         │       │   │   ├── frame/
         │       │   │   │   ├── frame_command_parser_factory.py
         │       │   │   │   ├── frame_reset_command_parser.py
         │       │   │   │   ├── frame_set_command_parser.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── icommand_parser.py
         │       │   │   ├── icommand_parser_provider.py
         │       │   │   ├── __init__.py
         │       │   │   ├── macro/
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── jump_command_parser.py
         │       │   │   │   ├── macro_command_parser_factory.py
         │       │   │   │   ├── pallet_def_command_parser.py
         │       │   │   │   └── pallet_move_command_parser.py
         │       │   │   ├── motion/
         │       │   │   │   ├── approach_command_parser.py
         │       │   │   │   ├── arc_command_parser.py
         │       │   │   │   ├── home_command_parser.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── jog_command_parser.py
         │       │   │   │   ├── joint_move_command_parser.py
         │       │   │   │   ├── linear_move_command_parser.py
         │       │   │   │   ├── motion_command_parser_factory.py
         │       │   │   │   ├── probe_command_parser.py
         │       │   │   │   └── retract_command_parser.py
         │       │   │   ├── parameter/
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── parameter_extractor.py
         │       │   │   └── tool/
         │       │   │       ├── __init__.py
         │       │   │       ├── pump_command_parser.py
         │       │   │       ├── tool_command_parser.py
         │       │   │       ├── tool_command_parser_factory.py
         │       │   │       └── valve_command_parser.py
         │       │   ├── __init__.py
         │       │   ├── instruction/
         │       │   │   ├── iinstruction_line_parser.py
         │       │   │   ├── __init__.py
         │       │   │   ├── instruction_line_parser.py
         │       │   │   └── instruction_line_parser_factory.py
         │       │   ├── iscara_parser.py
         │       │   ├── lexer/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_lexer.py
         │       │   │   ├── scara_lexer.py
         │       │   │   └── scara_lexer_factory.py
         │       │   ├── scara_parser.py
         │       │   ├── scara_parser_factory.py
         │       │   └── splitter/
         │       │       ├── __init__.py
         │       │       ├── itoken_line_splitter.py
         │       │       ├── token_line_splitter.py
         │       │       └── token_line_splitter_factory.py
         │       ├── protocol/
         │       │   ├── ibinary_frame_builder.py
         │       │   ├── ibinary_frame_parser.py
         │       │   ├── ibinary_payload_unpacker.py
         │       │   └── __init__.py
         │       └── trajectory/
         │           ├── discretization/
         │           │   ├── __init__.py
         │           │   ├── ishape_discretizer.py
         │           │   ├── shape_discretizer.py
         │           │   └── shape_discretizer_factory.py
         │           ├── __init__.py
         │           ├── metrics/
         │           │   ├── bottleneck/
         │           │   │   ├── imotion_bottleneck_detector.py
         │           │   │   ├── __init__.py
         │           │   │   ├── motion_bottleneck_detector.py
         │           │   │   └── motion_bottleneck_detector_factory.py
         │           │   ├── cycle/
         │           │   │   ├── cycle_time_calculator.py
         │           │   │   ├── cycle_time_calculator_factory.py
         │           │   │   ├── icycle_time_calculator.py
         │           │   │   └── __init__.py
         │           │   ├── __init__.py
         │           │   ├── profile/
         │           │   │   ├── axis_speed_profile_analyzer.py
         │           │   │   ├── axis_speed_profile_analyzer_factory.py
         │           │   │   ├── iaxis_speed_profile_analyzer.py
         │           │   │   └── __init__.py
         │           │   ├── summary/
         │           │   │   ├── __init__.py
         │           │   │   ├── itrajectory_cycle_summary_builder.py
         │           │   │   ├── trajectory_cycle_summary_builder.py
         │           │   │   └── trajectory_cycle_summary_builder_factory.py
         │           │   └── trajectory_metrics.py
         │           ├── plan/
         │           │   ├── __init__.py
         │           │   ├── itrajectory_mutable.py
         │           │   ├── itrajectory_plan.py
         │           │   ├── itrajectory_plan_factory.py
         │           │   ├── itrajectory_read_only.py
         │           │   ├── trajectory_plan.py
         │           │   └── trajectory_plan_factory.py
         │           └── validation/
         │               ├── feedrate/
         │               │   ├── feedrate_validator.py
         │               │   ├── feedrate_validator_factory.py
         │               │   ├── ifeedrate_validator.py
         │               │   └── __init__.py
         │               ├── __init__.py
         │               ├── itrajectory_validator.py
         │               ├── plan/
         │               │   ├── __init__.py
         │               │   ├── itrajectory_plan_validator.py
         │               │   ├── trajectory_plan_validator.py
         │               │   └── trajectory_plan_validator_factory.py
         │               ├── trajectory_validator.py
         │               ├── trajectory_validator_factory.py
         │               └── waypoint/
         │                   ├── __init__.py
         │                   ├── iwaypoint_validator.py
         │                   ├── waypoint_validator.py
         │                   └── waypoint_validator_factory.py
         ├── engine.py
         ├── infrastructure/
         │   ├── cli/
         │   │   ├── engine.py
         │   │   ├── icli.py
         │   │   ├── __init__.py
         │   │   ├── repl/
         │   │   │   ├── compiler/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── irepl_single_command_compiler.py
         │   │   │   │   ├── repl_single_command_compiler.py
         │   │   │   │   └── repl_single_command_compiler_factory.py
         │   │   │   ├── dispatch/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── irepl_command_dispatcher.py
         │   │   │   │   ├── repl_command_dispatcher.py
         │   │   │   │   └── repl_command_dispatcher_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── input/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── irepl_line_reader.py
         │   │   │   │   ├── repl_line_reader.py
         │   │   │   │   └── repl_line_reader_factory.py
         │   │   │   ├── presentation/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── irepl_response_presenter.py
         │   │   │   │   ├── repl_response_presenter.py
         │   │   │   │   └── repl_response_presenter_factory.py
         │   │   │   └── transmission/
         │   │   │       ├── __init__.py
         │   │   │       ├── irepl_frame_transmitter.py
         │   │   │       ├── repl_frame_transmitter.py
         │   │   │       └── repl_frame_transmitter_factory.py
         │   │   └── setup/
         │   │       ├── bundle.py
         │   │       ├── dep_validator.py
         │   │       ├── dependencies.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       ├── keys.py
         │   │       ├── opt_validator.py
         │   │       ├── options.py
         │   │       ├── registry.py
         │   │       └── validator.py
         │   ├── command/
         │   │   ├── command_bundle.py
         │   │   ├── command_bundle_factory.py
         │   │   ├── compile/
         │   │   │   ├── compile_command_definition.py
         │   │   │   ├── compile_command_executor.py
         │   │   │   ├── compile_command_executor_factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── inspection/
         │   │   │   │   ├── framing/
         │   │   │   │   │   ├── frame_header_formatter.py
         │   │   │   │   │   ├── frame_header_formatter_factory.py
         │   │   │   │   │   ├── frame_trailer_formatter.py
         │   │   │   │   │   ├── frame_trailer_formatter_factory.py
         │   │   │   │   │   ├── hex_stream_formatter.py
         │   │   │   │   │   ├── hex_stream_formatter_factory.py
         │   │   │   │   │   ├── iframe_header_formatter.py
         │   │   │   │   │   ├── iframe_trailer_formatter.py
         │   │   │   │   │   ├── ihex_stream_formatter.py
         │   │   │   │   │   └── __init__.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── payload/
         │   │   │   │   │   ├── ijoint_steps_payload_formatter.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── ipayload_dispatcher_formatter.py
         │   │   │   │   │   ├── itool_command_payload_formatter.py
         │   │   │   │   │   ├── joint_steps_payload_formatter.py
         │   │   │   │   │   ├── joint_steps_payload_formatter_factory.py
         │   │   │   │   │   ├── payload_dispatcher_formatter.py
         │   │   │   │   │   ├── payload_dispatcher_formatter_factory.py
         │   │   │   │   │   ├── tool_command_payload_formatter.py
         │   │   │   │   │   └── tool_command_payload_formatter_factory.py
         │   │   │   │   └── presentation/
         │   │   │   │       ├── frame_step_presenter.py
         │   │   │   │       ├── frame_step_presenter_factory.py
         │   │   │   │       ├── iframe_step_presenter.py
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── iprogram_inspection_presenter.py
         │   │   │   │       ├── program_inspection_presenter.py
         │   │   │   │       └── program_inspection_presenter_factory.py
         │   │   │   └── telemetry/
         │   │   │       ├── compile_telemetry_formatter.py
         │   │   │       ├── compile_telemetry_formatter_factory.py
         │   │   │       ├── icompile_telemetry_formatter.py
         │   │   │       └── __init__.py
         │   │   ├── disassemble/
         │   │   │   ├── disassemble_command_definition.py
         │   │   │   ├── disassemble_command_executor.py
         │   │   │   ├── disassemble_command_executor_factory.py
         │   │   │   ├── format/
         │   │   │   │   ├── disassemble_summary_formatter.py
         │   │   │   │   ├── disassemble_summary_formatter_factory.py
         │   │   │   │   ├── idisassemble_summary_formatter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── __init__.py
         │   │   ├── export/
         │   │   │   ├── export_command_definition.py
         │   │   │   ├── export_command_executor.py
         │   │   │   ├── export_command_executor_factory.py
         │   │   │   └── __init__.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── info/
         │   │   │   ├── info_command_definition.py
         │   │   │   ├── info_command_executor.py
         │   │   │   ├── info_command_executor_factory.py
         │   │   │   └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── lint/
         │   │   │   ├── __init__.py
         │   │   │   ├── lint_command_definition.py
         │   │   │   ├── lint_command_executor.py
         │   │   │   └── lint_command_executor_factory.py
         │   │   └── repl/
         │   │       ├── __init__.py
         │   │       ├── repl_command_definition.py
         │   │       ├── repl_command_executor.py
         │   │       └── repl_command_executor_factory.py
         │   ├── communication/
         │   │   ├── __init__.py
         │   │   └── protocol/
         │   │       ├── binary/
         │   │       │   ├── binary_struct_format.py
         │   │       │   ├── builder/
         │   │       │   │   ├── binary_frame_builder.py
         │   │       │   │   ├── binary_frame_builder_factory.py
         │   │       │   │   └── __init__.py
         │   │       │   ├── checksum/
         │   │       │   │   ├── crc16_ccitt.py
         │   │       │   │   └── __init__.py
         │   │       │   ├── __init__.py
         │   │       │   └── parser/
         │   │       │       ├── binary_frame_assembler.py
         │   │       │       ├── binary_frame_assembler_factory.py
         │   │       │       ├── binary_frame_parser.py
         │   │       │       ├── binary_frame_parser_factory.py
         │   │       │       ├── binary_payload_unpacker.py
         │   │       │       ├── binary_payload_unpacker_factory.py
         │   │       │       ├── ibinary_frame_assembler.py
         │   │       │       ├── __init__.py
         │   │       │       └── parser_state.py
         │   │       └── __init__.py
         │   ├── config/
         │   │   ├── scaralang.cfg
         │   │   └── scaralang.logo
         │   └── __init__.py
         ├── __init__.py
         ├── py.typed
         └── setup/
             ├── bundle.py
             ├── dep_validator.py
             ├── dependencies.py
             ├── factory.py
             ├── __init__.py
             ├── keys.py
             ├── opt_validator.py
             ├── options.py
             ├── registry.py
             └── validator.py

     117 directories, 545 files

🏗 Architecture & SOLID Principles
--------------------------------------------------------------------------------

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │                   CLI / Inbound Adapters                    │
    │        (Compile, Disassemble, Lint, Info, Export, REPL)     │
    └──────────────┬───────────────────────────────┬──────────────┘
                   │ Depends on Role Protocols     │
                   ▼                               ▼
    ┌──────────────────────────────┐┌─────────────────────────────┐
    │     IScaraDslLinter          ││  IScaraDslBinaryCompiler    │
    │   (Validation & Diagnostics) ││  (Plan / Binary Generation) │
    └──────────────┬───────────────┘└──────────────┬──────────────┘
                   │                               │
                   ▼                               ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    Application Services                     │
    │  ┌────────────────────┐ ┌─────────────────┐ ┌─────────────┐ │
    │  │     ScaraLexer     │ │   ScaraParser   │ │ScaraCompiler│ │
    │  │   (Token Stream)   │ │(Command Parsers)│ │(Macro Expan)│ │
    │  └────────────────────┘ └─────────────────┘ └─────────────┘ │
    │  ┌────────────────────┐ ┌─────────────────┐ ┌─────────────┐ │
    │  │   BinaryCompiler   │ │ScaraDisassembler│ │ExportDispatc│ │
    │  │  (Step Generator)  │ │(Frame Breakdown)│ │(Multi-target│ │
    │  └────────────────────┘ └─────────────────┘ └─────────────┘ │
    └──────────────────────────────┬──────────────────────────────┘
                                   │ Operates on Pure Models
                                   ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     Pure Domain Models                      │
    │    (ScaraProgram, BinaryProgram, Waypoint, DisassemblySum,  │
    │     InstructionParam, ScaraCommandType, MessageId, Zone)    │
    └─────────────────────────────────────────────────────────────┘

SOLID Principles Compliance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **S — Single Responsibility Principle (SRP)**:
  Every module, class, and service has exactly one clearly bounded reason to change. Parser and compiler logic is decomposed into dedicated handlers (``MotionCommandParser``, ``ConfigCommandParser``, ``PalletMacroExpander``, ``StepDiscretizer``) rather than a monolithic interpreter. Strict limit of <= 15 methods per class across the entire codebase enforced by automated Quality Gate.
* **O — Open/Closed Principle (OCP)**:
  The DSL parser, macro expanders, and exporters are open for extension without modifying existing code. Extensible Chain of Responsibility and dispatcher pattern allow registering new instruction handlers and export targets seamlessly.
* **L — Liskov Substitution Principle (LSP)**:
  Pure structural subtyping via Python ``@runtime_checkable Protocol`` definitions. Concrete classes never inherit from abstract protocols, ensuring complete structural interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  Fat facade ``IScaraDslService`` is segregated into focused role protocols (``IScaraDslBinaryCompiler``, ``IScaraDslDisassembler``, ``IScaraDslLinter``, ``IScaraDslInfoProvider``, ``IScaraDslCompiler``, ``IScaraPlanExporter``). Clients depend strictly on the minimal methods they call.
* **D — Dependency Inversion Principle (DIP)**:
  High-level domain services and CLI executors depend strictly on abstract protocols, never on concrete implementations. All infrastructure dependencies are injected via constructor Dependency Injection (Zero-Fallback DI).

Automated Quality Gates (``run_quality_gates.sh``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Every build is validated against 4 strict automated quality gates:

1. **Structural Protocols Gate (``interfaces_checker.py``)**: Verifies 100% compliance with ``@runtime_checkable Protocol`` structural typing across concrete implementations.
2. **Interface Segregation Gate (``isp_checker.py``)**: Enforces ISP compliance and verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate (``limits_checker.py``)**: Enforces file length, method count, and line length limits (<= 150 characters).
4. **Single Responsibility Gate (``srp_checker.py``)**: Strictly enforces <= 15 methods per class and logical method line limits.

✨ Features
--------------------------------------------------------------------------------

* **High-Level SCARA DSL Toolchain**: Lexer, Tokenizer, Line Splitter, AST Parser, Linter, and Semantic Validator for human-readable SCARA motion scripts (``.scara``).
* **Deterministic Bytecode Compiler**: Direct translation of high-level Cartesian DSL trajectories into discrete stepper motor joint step blocks (``JointSteps``, ``Step``, ``BinaryProgram``).
* **SCARA Binary Wire Protocol Codec**: High-performance streaming frame parser, payload unpacker, frame builder, and CRC-16-CCITT integrity verification (``0xAA 0x55`` header framing).
* **Multi-Target Trajectory Exporter**: Export robotic trajectories into industrial G-code, CSV time-series data, JSON trajectory bundles, and SVG vector toolpaths.
* **Interactive Motion REPL Console**: Terminal-based interactive console (``scarac repl``) for real-time single-command compilation, inspection, and frame transmission.
* **Single Source of Truth (SSoT)**: Seamless domain and codec foundation shared between ``scarajectory`` (Desktop Studio), ``scaraemu`` (Digital Twin Simulator), and ``dof2bot/scara`` (RP2040 firmware).
* **Zero GUI Dependencies**: 100% headless, clean architecture design with zero Tkinter, Qt, or graphics dependencies.
* **Strict Quality & SOLID Standards**: 100% structural protocol conformance, 99% test coverage, and 10.00 / 10.00 Pylint score.

📜 SCARA Domain-Specific Language (DSL) & ``.scara`` Programs
--------------------------------------------------------------------------------

**scaralang** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the ``.scara`` extension and compiled into validated Cartesian trajectories via a clean AST pipeline:

.. code-block:: text

    ┌─────────────────────────┐
    │      .scara Source      │
    └────────────┬────────────┘
      ScaraLexer │
                 ▼
    ┌─────────────────────────┐
    │      Token Stream       │
    └────────────┬────────────┘
     ScaraParser │
                 ▼
    ┌─────────────────────────┐
    │       Abstract AST      │
    └────────────┬────────────┘
   ScaraCompiler │ (Macros + Kinematics) 
                 ▼
    ┌─────────────────────────┐
    │      TrajectoryPlan     │
    │(Waypoints & Discretize) │
    └────────────┬────────────┘
  BinaryCompiler │ (Step Discretization)
                 ▼
    ┌─────────────────────────┐
    │      BinaryProgram      │
    │(Wire Frames & Bytecode) │
    └─────────────────────────┘

SCARA DSL Instruction Reference
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the exhaustive syntax specification, boundary constraints, and compiler rules, see `LANGUAGE_REFERENCE.md`.

.. list-table:: SCARA DSL Instruction Reference
   :widths: 15 35 25 35
   :header-rows: 1

   * - Category
     - Instruction & Syntax
     - Parameters
     - Description
   * - **Motion**
     - ``MOVE_J X <x> Y <y> Z <z> [P <phi>]``
     - ``X, Y, Z`` (mm), ``P`` (deg)
     - Rapid non-interpolated Cartesian joint motion.
   * -
     - ``MOVE_L X <x> Y <y> Z <z> [P <phi>]``
     - ``X, Y, Z`` (mm), ``P`` (deg)
     - Linear continuous path interpolated motion.
   * -
     - ``ARC_CW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]``
     - ``X, Y`` target, ``I, J`` center offset
     - Clockwise circular arc interpolation in XY plane.
   * -
     - ``ARC_CCW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]``
     - ``X, Y`` target, ``I, J`` center offset
     - Counter-clockwise circular arc interpolation.
   * -
     - ``APPROACH DIST <d>``
     - ``DIST`` (mm, > 0)
     - Relative vertical descent along -Z axis.
   * -
     - ``RETRACT DIST <d>``
     - ``DIST`` (mm, > 0)
     - Relative vertical ascent along +Z axis.
   * -
     - ``JOG_AXIS <X|Y|Z|PHI> <step>``
     - Axis name, step displacement
     - Incremental single-axis manual jog move.
   * -
     - ``JOG_JOINT <1|2|3|4> <deg>``
     - Joint ID (1..4), angle (deg)
     - Incremental individual joint rotational jog.
   * -
     - ``PROBE [SPEED <s>] [DIST <d>]``
     - ``SPEED`` (mm/s), ``DIST`` (mm)
     - Tactile surface contact search along -Z axis.
   * - **Macros**
     - ``JUMP X <x> Y <y> Z <z> [ARCH <h>]``
     - ``X, Y, Z``, ``ARCH`` apex clearance
     - Smooth 3D parabolic pick-and-place arch motion.
   * -
     - ``PALLET_DEF <id> ROWS <r> COLS <c> DX <dx> DY <dy>``
     - Matrix dimensions & grid spacing
     - Defines structured 2D Cartesian pallet matrix.
   * -
     - ``MOVE_PALLET <id> INDEX <i>``
     - Pallet identifier, 1-based index
     - Direct positioning to pallet matrix cell.
   * - **Actuators**
     - ``PUMP <ON|OFF>``
     - ``ON`` or ``OFF``
     - Energizes or cuts end-effector vacuum pump.
   * -
     - ``VALVE <ON|OFF>``
     - ``ON`` or ``OFF``
     - Opens or closes pneumatic release blow-off valve.
   * -
     - ``TOOL <UP|DOWN>``
     - ``UP`` or ``DOWN``
     - Actuates tool head vertical pneumatic slide stage.
   * -
     - ``TOOL_ORIENT <AUTO|TANGENT|FIXED>``
     - Tracking mode
     - Configures 4th-axis tool yaw orientation mode.
   * - **Dynamics**
     - ``SPEED <RAPID|WORK> <val>``
     - ``RAPID`` or ``WORK``, feedrate (mm/s)
     - Configures travel or working linear feedrate.
   * -
     - ``ACCEL <val>``
     - ``val`` (mm/s²)
     - Configures linear path acceleration limit.
   * -
     - ``OVERRIDE <percent>``
     - ``percent`` (10% - 200%)
     - Scales path execution velocity dynamically.
   * -
     - ``ZONE <OFF|FINE|EXACT|Z1..Z50>``
     - Corner rounding tolerance (mm)
     - Corner tolerance zone for trajectory smoothing.
   * - **Kinematics**
     - ``CONFIG ELBOW <LEFT|RIGHT>``
     - ``LEFT`` or ``RIGHT``
     - Sets arm kinematic inverse solution branch.
   * -
     - ``CONFIG MOTOR <OPEN_LOOP|CLOSED_LOOP>``
     - Drive control mode
     - Selects open-loop microstepping or closed-loop FOC.
   * -
     - ``FRAME X <x> Y <y> Z <z> [PHI <p>]``
     - Cartesian offset coordinates
     - Defines user workpiece reference coordinate frame.
   * -
     - ``FRAME_RESET``
     - None
     - Resets coordinate system to base world origin.
   * -
     - ``HOME``
     - None
     - Triggers complete multi-axis homing routine.
   * - **Safety & Flow**
     - ``WAIT <ms>`` / ``WAIT_MS <ms>``
     - ``ms`` (milliseconds)
     - Dwells execution for specified hardware duration.
   * -
     - ``SYNC``
     - None
     - Trajectory execution barrier (drains buffer).
   * -
     - ``HOLD``
     - None
     - Trajectory feed hold; pauses running motion.
   * -
     - ``RESUME``
     - None
     - Resumes previously suspended trajectory.
   * -
     - ``ESTOP``
     - None
     - Immediate emergency stop and motion abort.
   * -
     - ``ENABLE``
     - None
     - Energizes motor driver stages (holding torque).
   * -
     - ``DISABLE``
     - None
     - De-energizes motor driver stages (free movement).

Example ``.scara`` Program: Industrial Pick & Place
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text

    # ----------------------------------------------------
    # Industrial Pick-and-Place Cycle with Pneumatic Grip
    # ----------------------------------------------------
    CONFIG ELBOW LEFT
    SPEED RAPID 180.0
    SPEED WORK 60.0
    ACCEL 400.0
    OVERRIDE 100

    # Home robot to reference position
    HOME

    # Rapid move above pick feeder station
    MOVE_J X 140.0 Y -30.0 Z 35.0
    APPROACH DIST 30.0

    # Engage suction cup and pause for vacuum seal
    PUMP ON
    WAIT 200

    # Retract with part
    RETRACT DIST 30.0

    # Smooth 3D parabolic arch transfer to drop location
    JUMP X 180.0 Y 30.0 Z 5.0 ARCH 40.0

    # Release part with air pulse
    PUMP OFF
    VALVE ON
    WAIT 100
    VALVE OFF

    # Retract to safe transit altitude
    RETRACT DIST 30.0
    HOME

📡 SCARA Binary Wire Protocol & Codec
--------------------------------------------------------------------------------

All binary wire communication between **scaralang**, **scarajectory**, **scaraemu**, and physical robot firmware is governed by deterministic packet framing:

Frame Header & Wire Format
^^^^^^^^^^^^^^^^^^^^^^^^^^

Each binary frame consists of a 4-byte header, variable payload, and 2-byte CRC-16-CCITT checksum:

.. code-block:: text

    ┌──────────────┬──────────────┬──────────────┬──────────────────┬──────────────┐
    │  SOF1 (0xAA) │  SOF2 (0x55) │  Msg ID (1B) │  Payload Len (1B)│ Payload (NB) │ ... CRC16 (2B)
    └──────────────┴──────────────┴──────────────┴──────────────────┴──────────────┘

Message Types & Payload Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Binary Message Types
   :widths: 15 20 35 30
   :header-rows: 1

   * - Message ID
     - Enum Identifier
     - Payload Structure
     - Description
   * - ``0x01``
     - ``JOINT_STEPS``
     - ``Step[n]`` (8 bytes per step: ΔS1, ΔS2, ΔS3, ΔS4)
     - Coordinated stepper motor joint step block.
   * - ``0x02``
     - ``TOOL_COMMAND``
     - ``ToolId (1B), Action (1B), Param (2B)``
     - End-effector actuator trigger (vacuum, gripper, valve).
   * - ``0x03``
     - ``ESTOP``
     - Empty (``0 bytes``)
     - Immediate hardware emergency stop.
   * - ``0x04``
     - ``PAUSE``
     - Empty (``0 bytes``)
     - Pause execution / feed hold.
   * - ``0x05``
     - ``RESUME``
     - Empty (``0 bytes``)
     - Resume paused trajectory execution.
   * - ``0x06``
     - ``HEARTBEAT``
     - ``Sequence (4B), Status (1B)``
     - Real-time link health and operational state beacon.
   * - ``0x07``
     - ``SYNC``
     - ``Timestamp (4B)``
     - Clock synchronization and timestamp alignment.

Hardware Execution & Motor Actuation Targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Binary wire frames generated by **scaralang** stream directly over UART / USB-CDC to the physical **``scara_base``** firmware running on the Raspberry Pi Pico (RP2040), which coordinates motor actuation across two configurable drive modes:

* **Open-Loop Stepper Mode (TMC2209):** Coordinated microstepping pulses generated by RP2040 PIO hardware state machines driving TMC2209 STEP/DIR stages for ultra-silent operation.
* **Closed-Loop Stepper Mode (MKS SERVO42D over CAN Bus):** NEMA stepper motors equipped with **MKS SERVO42D** closed-loop modules communicating with the Raspberry Pi Pico over a high-speed differential **CAN bus** (CAN_H / CAN_L). This guarantees 100% elimination of lost steps, hardware PID closed-loop position correction, and real-time following-error telemetry.

📊 Code coverage
--------------------------------------------------------------------------------

.. csv-table:: Code coverage
   :file: coverage_table.csv
   :widths: 60, 10, 10, 20
   :header-rows: 1

🛠 Usage
--------------------------------------------------------------------------------

Install package

.. code-block:: bash

    pip3 install scaralang

CLI Tool (scarac / scaralang)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    # Display general help and available subcommands
    scarac --help

    # Validate syntax and run static diagnostic lint checks
    scarac lint program.scara

    # Compile DSL program to packed binary execution file (.bin)
    scarac compile program.scara -o program.bin

    # Compile with verbose wire frame inspection and telemetry metrics
    scarac compile program.scara -o program.bin --verbose

    # Disassemble binary bytecode file into human-readable frame breakdown
    scarac disassemble program.bin --summary

    # Export trajectory to industrial G-code, CSV time-series, JSON, or SVG
    scarac export program.scara --format GCODE -o program.gcode
    scarac export program.scara --format CSV -o trajectory.csv
    scarac export program.scara --format JSON -o bundle.json
    scarac export program.scara --format SVG -o toolpath.svg

    # Inspect toolchain info, supported commands, and grammar version
    scarac info

    # Launch interactive SCARA DSL motion REPL console
    scarac repl

Python Library API
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from scaralang.setup.factory import ScaralangBundleFactory
    from scaralang.engine import Scaralang
    from scaralang.core.service.dsl.scara_dsl_service_factory import (
        ScaraDslServiceFactory,
    )

    # Initialize full DSL service via Composition Root factory
    dsl_service = ScaraDslServiceFactory.create()

    # Lint a script string
    diagnostics = dsl_service.lint(
        "HOME\nMOVE_J X:100.0 Y:150.0 Z:20.0 SPEED:FAST\n"
    )
    if not diagnostics:
        print("Syntax & static semantics: OK")

    # Compile to binary wire payload
    binary_data, telemetry = dsl_service.compile_to_binary(
        "HOME\nMOVE_L X:50.0 Y:80.0 Z:10.0 SPEED:SLOW\n"
    )
    print(
        f"Compiled {len(binary_data)} bytes in {telemetry.compilation_duration_ms:.2f} ms"
    )

📚 Docs
--------------------------------------------------------------------------------

`ReadTheDocs Documentation <https://scaralang.readthedocs.io/en/latest/>`_

👥 Contributing
--------------------------------------------------------------------------------

`Contributing to scaralang <CONTRIBUTING.md>`_

📄 Copyright and licence
--------------------------------------------------------------------------------

|gplv3 license| |apache license|

Copyright (C) 2026 by `vroncevic.github.io/scaralang <https://vroncevic.github.io/scaralang>`_

**scaralang** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.