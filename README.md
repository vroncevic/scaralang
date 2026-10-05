# SCARA Robotics Domain-Specific Language (DSL) Toolchain & Binary Protocol Codec

<img align="right" src="https://raw.githubusercontent.com/vroncevic/scaralang/dev/docs/scaralang_logo.png" width="25%">

**scaralang** is a standalone, lightweight, GUI-independent Python toolchain and compiler for the **SCARA Robotics Domain-Specific Language (DSL)**, combined with the official **SCARA Wire Binary Protocol Codec**.

Developed in **[python](https://www.python.org/)** code.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![scaralang python checker](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python_checker.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python_checker.yml) [![scaralang package checker](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_package_checker.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_package_checker.yml) [![scaralang interface checker](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_interface_checker.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_interface_checker.yml) [![scaralang isp checker](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_isp_checker.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_isp_checker.yml) [![scaralang srp checker](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_srp_checker.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_srp_checker.yml) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/scaralang.svg)](https://github.com/vroncevic/scaralang/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/scaralang.svg)](https://github.com/vroncevic/scaralang/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [🚀 Installation](#-installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [📦 Dependencies](#-dependencies)
- [📁 Tool structure](#-tool-structure)
  - [🏗 Architecture & SOLID Principles](#-architecture--solid-principles)
    - [SOLID Principles Compliance](#solid-principles-compliance)
    - [Automated Quality Gates (`run_quality_gates.sh`)](#automated-quality-gates-run_quality_gatessh)
  - [✨ Features](#-features)
  - [📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs](#-scara-domain-specific-language-dsl--scara-programs)
    - [SCARA DSL Instruction Quick Reference](#scara-dsl-instruction-quick-reference)
    - [Example `.scara` Program: Industrial Pick & Place](#example-scara-program-industrial-pick--place)
  - [📡 SCARA Binary Wire Protocol & Codec](#-scara-binary-wire-protocol--codec)
    - [Frame Header & Wire Format](#frame-header--wire-format)
    - [Message Types & Payload Structure](#message-types--payload-structure)
    - [Hardware Execution & Motor Actuation Targets](#hardware-execution--motor-actuation-targets)
- [🛡️ Error Handling & Diagnostic Architecture](#-error-handling--diagnostic-architecture)
  - [Domain Exception Hierarchy](#domain-exception-hierarchy)
  - [Dedicated Command Error Handlers](#dedicated-command-error-handlers)
  - [Categorized Diagnostics & Formatted Messages](#categorized-diagnostics--formatted-messages)
  - [Python Library API: Error Handling Example](#python-library-api-error-handling-example)
- [📊 Code coverage](#-code-coverage)
- [🛠 Usage](#-usage)
    - [CLI Tool (`scarac` / `scaralang`)](#cli-tool-scarac--scaralang)
    - [CLI Subcommand Reference](#cli-subcommand-reference)
    - [Python Library API](#python-library-api)
- [📚 Docs](#-docs)
- [👥 Contributing](#-contributing)
- [📄 Copyright and licence](#-copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### 🚀 Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/scaralang/dev/docs/debtux.png)

[![scaralang python3 build](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python3_build.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python3_build.yml)

Currently there are three ways to install package
* Install process based on using pip mechanism
* Install process based on build mechanism
* Install process based on setup.py mechanism
* Install process based on docker mechanism

##### Install using pip

**scaralang** is located at **[pypi.org](https://pypi.org/project/scaralang/)**.

You can install by using pip

```bash
# python3
pip3 install scaralang
```

##### Install using build

Navigate to release **[page](https://github.com/vroncevic/scaralang/releases/)** download and extract release archive.

To install **scaralang** type the following

```bash
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
chmod 755 /usr/local/lib/python3.10/dist-packages/usr/local/bin/scarac.py
ln -s /usr/local/lib/python3.10/dist-packages/usr/local/bin/scarac.py /usr/local/bin/scarac
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/scaralang/releases)** download and extract release archive.

To install **scaralang** locate and run setup.py with arguments

```bash
tar xvzf scaralang-x.y.z.tar.gz
cd scaralang-x.y.z
# python3
pip3 install -r requirements.txt
python3 setup.py install_lib
python3 setup.py install_egg_info
```

##### Install using docker

You can use Dockerfile to create image/container.

### 📦 Dependencies

**scaralang** requires next modules and libraries

* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

### 📁 Tool structure

**scaralang** is based on OOP and Clean Architecture.

Tool structure

<details>
<summary><b>Click to expand framework structure</b></summary>

```bash
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
         │   │   │   │   ├── axis_peak_steps.py
         │   │   │   │   ├── binary_program_telemetry.py
         │   │   │   │   ├── disassembled_frame.py
         │   │   │   │   ├── disassembly_summary.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── parsed_command_token.py
         │   │   │   │   ├── program.py
         │   │   │   │   └── step.py
         │   │   │   ├── compiler/
         │   │   │   │   ├── arc_geometry.py
         │   │   │   │   ├── compiler_blend_state.py
         │   │   │   │   ├── compiler_pose_state.py
         │   │   │   │   ├── compiler_speed_state.py
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
         │   │   │   │   ├── lint_tool_state.py
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
         │   │   ├── exceptions/
         │   │   │   ├── __init__.py
         │   │   │   ├── scara_error.py
         │   │   │   ├── scara_export_error.py
         │   │   │   ├── scara_kinematics_error.py
         │   │   │   ├── scara_protocol_error.py
         │   │   │   ├── scara_semantic_error.py
         │   │   │   └── scara_syntax_error.py
         │   │   ├── __init__.py
         │   │   ├── kinematics/
         │   │   │   ├── elbow_config.py
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_angle_bounds.py
         │   │   │   ├── link_dimensions.py
         │   │   │   ├── point_2d.py
         │   │   │   ├── point_3d.py
         │   │   │   ├── scara_bounds.py
         │   │   │   ├── singularity_margins.py
         │   │   │   ├── speed_limits.py
         │   │   │   ├── transmission_parameters.py
         │   │   │   └── vertical_bounds.py
         │   │   ├── motor/
         │   │   │   ├── axis_mask.py
         │   │   │   ├── __init__.py
         │   │   │   ├── motor_config.py
         │   │   │   ├── motor_drive_mode.py
         │   │   │   ├── motor_drive_mode_alias.py
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
         │   │   │   ├── repl_pose_state.py
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
         │       │   ├── dsl/
         │       │   │   ├── __init__.py
         │       │   │   ├── iscara_dsl_binary_compiler.py
         │       │   │   ├── iscara_dsl_compiler.py
         │       │   │   ├── scara_dsl_binary_compiler.py
         │       │   │   ├── scara_dsl_binary_compiler_factory.py
         │       │   │   ├── scara_dsl_compiler.py
         │       │   │   └── scara_dsl_compiler_factory.py
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
         │       │   ├── plan/
         │       │   │   ├── __init__.py
         │       │   │   ├── itrajectory_plan_compiler.py
         │       │   │   ├── trajectory_plan_compiler.py
         │       │   │   └── trajectory_plan_compiler_factory.py
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
         │       ├── decompiler/
         │       │   ├── frame_decompiler.py
         │       │   ├── frame_decompiler_factory.py
         │       │   ├── iframe_decompiler.py
         │       │   ├── __init__.py
         │       │   ├── iscara_decompiler.py
         │       │   ├── scara_decompiler.py
         │       │   └── scara_decompiler_factory.py
         │       ├── disassembler/
         │       │   ├── frame_detail_decoder.py
         │       │   ├── frame_detail_decoder_factory.py
         │       │   ├── iframe_detail_decoder.py
         │       │   ├── __init__.py
         │       │   ├── iscara_disassembler.py
         │       │   ├── scara_disassembler.py
         │       │   └── scara_disassembler_factory.py
         │       ├── exporter/
         │       │   ├── csv/
         │       │   │   ├── csv_trajectory_exporter.py
         │       │   │   ├── csv_trajectory_exporter_factory.py
         │       │   │   ├── icsv_trajectory_exporter.py
         │       │   │   └── __init__.py
         │       │   ├── export_dispatcher_bundle.py
         │       │   ├── gcode/
         │       │   │   ├── gcode_exporter.py
         │       │   │   ├── gcode_exporter_factory.py
         │       │   │   ├── igcode_exporter.py
         │       │   │   └── __init__.py
         │       │   ├── __init__.py
         │       │   ├── iscara_exporter.py
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
         │       │   ├── scara_exporter.py
         │       │   ├── scara_exporter_factory.py
         │       │   └── svg/
         │       │       ├── __init__.py
         │       │       ├── isvg_trajectory_exporter.py
         │       │       ├── svg_trajectory_exporter.py
         │       │       └── svg_trajectory_exporter_factory.py
         │       ├── info/
         │       │   ├── __init__.py
         │       │   ├── iscara_info_provider.py
         │       │   ├── scara_info_provider.py
         │       │   └── scara_info_provider_factory.py
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
         │       │   ├── scara_linter_factory.py
         │       │   └── script/
         │       │       ├── __init__.py
         │       │       ├── iscara_dsl_linter.py
         │       │       ├── iscara_dsl_validator.py
         │       │       ├── scara_script_validator.py
         │       │       └── scara_script_validator_factory.py
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
         │       ├── trajectory/
         │       │   ├── discretization/
         │       │   │   ├── __init__.py
         │       │   │   ├── ishape_discretizer.py
         │       │   │   ├── shape_discretizer.py
         │       │   │   └── shape_discretizer_factory.py
         │       │   ├── __init__.py
         │       │   ├── metrics/
         │       │   │   ├── bottleneck/
         │       │   │   │   ├── imotion_bottleneck_detector.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motion_bottleneck_detector.py
         │       │   │   │   └── motion_bottleneck_detector_factory.py
         │       │   │   ├── cycle/
         │       │   │   │   ├── cycle_time_calculator.py
         │       │   │   │   ├── cycle_time_calculator_factory.py
         │       │   │   │   ├── icycle_time_calculator.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── __init__.py
         │       │   │   ├── profile/
         │       │   │   │   ├── axis_speed_profile_analyzer.py
         │       │   │   │   ├── axis_speed_profile_analyzer_factory.py
         │       │   │   │   ├── iaxis_speed_profile_analyzer.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── summary/
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── itrajectory_cycle_summary_builder.py
         │       │   │   │   ├── trajectory_cycle_summary_builder.py
         │       │   │   │   └── trajectory_cycle_summary_builder_factory.py
         │       │   │   └── trajectory_metrics.py
         │       │   ├── plan/
         │       │   │   ├── __init__.py
         │       │   │   ├── itrajectory_mutable.py
         │       │   │   ├── itrajectory_plan.py
         │       │   │   ├── itrajectory_plan_factory.py
         │       │   │   ├── itrajectory_read_only.py
         │       │   │   ├── trajectory_plan.py
         │       │   │   └── trajectory_plan_factory.py
         │       │   └── validation/
         │       │       ├── feedrate/
         │       │       │   ├── feedrate_validator.py
         │       │       │   ├── feedrate_validator_factory.py
         │       │       │   ├── ifeedrate_validator.py
         │       │       │   └── __init__.py
         │       │       ├── __init__.py
         │       │       ├── itrajectory_validator.py
         │       │       ├── plan/
         │       │       │   ├── __init__.py
         │       │       │   ├── itrajectory_plan_validator.py
         │       │       │   ├── trajectory_plan_validator.py
         │       │       │   └── trajectory_plan_validator_factory.py
         │       │       ├── trajectory_validator.py
         │       │       ├── trajectory_validator_factory.py
         │       │       └── waypoint/
         │       │           ├── __init__.py
         │       │           ├── iwaypoint_validator.py
         │       │           ├── waypoint_validator.py
         │       │           └── waypoint_validator_factory.py
         │       └── transformation/
         │           ├── frame_transformer.py
         │           ├── frame_transformer_factory.py
         │           ├── iframe_transformer.py
         │           └── __init__.py
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
         │   │   │   ├── output/
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── irepl_output_writer.py
         │   │   │   │   ├── repl_output_writer.py
         │   │   │   │   └── repl_output_writer_factory.py
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
         │   │   │   ├── bundle.py
         │   │   │   ├── definition.py
         │   │   │   ├── error/
         │   │   │   │   ├── compile_error_handler.py
         │   │   │   │   ├── compile_error_handler_factory.py
         │   │   │   │   ├── icompile_error_handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
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
         │   │   ├── decompile/
         │   │   │   ├── definition.py
         │   │   │   ├── error/
         │   │   │   │   ├── decompile_error_handler.py
         │   │   │   │   ├── decompile_error_handler_factory.py
         │   │   │   │   ├── idecompile_error_handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
         │   │   │   └── __init__.py
         │   │   ├── disassemble/
         │   │   │   ├── definition.py
         │   │   │   ├── error/
         │   │   │   │   ├── disassemble_error_handler.py
         │   │   │   │   ├── disassemble_error_handler_factory.py
         │   │   │   │   ├── idisassemble_error_handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
         │   │   │   ├── format/
         │   │   │   │   ├── disassemble_summary_formatter.py
         │   │   │   │   ├── disassemble_summary_formatter_factory.py
         │   │   │   │   ├── idisassemble_summary_formatter.py
         │   │   │   │   └── __init__.py
         │   │   │   └── __init__.py
         │   │   ├── export/
         │   │   │   ├── definition.py
         │   │   │   ├── error/
         │   │   │   │   ├── export_error_handler.py
         │   │   │   │   ├── export_error_handler_factory.py
         │   │   │   │   ├── iexport_error_handler.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
         │   │   │   └── __init__.py
         │   │   ├── icommand_definition.py
         │   │   ├── icommand_executor.py
         │   │   ├── info/
         │   │   │   ├── definition.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
         │   │   │   └── __init__.py
         │   │   ├── __init__.py
         │   │   ├── lint/
         │   │   │   ├── definition.py
         │   │   │   ├── error/
         │   │   │   │   ├── ilint_error_handler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── lint_error_handler.py
         │   │   │   │   └── lint_error_handler_factory.py
         │   │   │   ├── executor.py
         │   │   │   ├── executor_factory.py
         │   │   │   └── __init__.py
         │   │   └── repl/
         │   │       ├── bundle.py
         │   │       ├── definition.py
         │   │       ├── executor.py
         │   │       ├── executor_factory.py
         │   │       └── __init__.py
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

     125 directories, 595 files
```
</details>

#### 🏗 Architecture & SOLID Principles

```
           ┌─────────────────────────────────────────────────────────────┐
           │                   CLI / Inbound Adapters                    │
           │        (Compile, Disassemble, Lint, Info, Export, REPL)     │
           └──────────────┬───────────────────────────────┬──────────────┘
                          │ Depends on Role Protocols     │
                          ▼                               ▼
           ┌──────────────────────────────┐┌─────────────────────────────┐
           │         IScaraLinter         ││        IScaraCompiler       │
           │  (Validation & Diagnostics)  ││ (Plan & Binary Generation)  │
           └──────────────┬───────────────┘└──────────────┬──────────────┘
                          │                               │
                          ▼                               ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       Application Services                             │
│  ┌────────────────────┐  ┌───────────────────┐  ┌───────────────────┐  │
│  │     ScaraLexer     │  │    ScaraParser    │  │   ScaraCompiler   │  │
│  │   (Token Stream)   │  │ (Command Parsers) │  │  (Macro Expander) │  │
│  └────────────────────┘  └───────────────────┘  └───────────────────┘  │
│  ┌────────────────────┐  ┌───────────────────┐  ┌───────────────────┐  │
│  │   BinaryCompiler   │  │ ScaraDisassembler │  │   ScaraExporter   │  │
│  │  (Step Generator)  │  │ (Frame Detail Dec)│  │ (Multi-target Exp)│  │
│  └────────────────────┘  └───────────────────┘  └───────────────────┘  │
└─────────────────────────────────┬──────────────────────────────────────┘
                                  │ Operates on Pure Models
                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Pure Domain Models                              │
│       (ScaraProgram, BinaryProgram, Waypoint, DisassemblySummary,      │
│        InstructionParam, ScaraCommandType, MessageId, ZoneMode)        │
└────────────────────────────────────────────────────────────────────────┘
```

##### SOLID Principles Compliance

* **S — Single Responsibility Principle (SRP)**:
  * Every module, class, and service has exactly one clearly bounded reason to change.
  * Parser and compiler logic is decomposed into dedicated handlers (`MotionCommandParser`, `ConfigCommandParser`, `PalletMacroExpander`, `StepDiscretizer`) rather than a monolithic interpreter.
  * Strict limit of $\le 15$ methods per class across the entire codebase enforced by automated Quality Gate.
* **O — Open/Closed Principle (OCP)**:
  * The DSL parser, macro expanders, and exporters are open for extension without modifying existing code.
  * Extensible Chain of Responsibility and dispatcher pattern allow registering new instruction handlers and export targets seamlessly.
* **L — Liskov Substitution Principle (LSP)**:
  * Pure structural subtyping via Python `@runtime_checkable Protocol` definitions. Concrete classes never inherit from abstract protocols, ensuring complete structural interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  * Unified role protocols (`IScaraCompiler`, `IScaraDecompiler`, `IScaraDisassembler`, `IScaraLinter`, `IScaraParser`, `IScaraLexer`, `IScaraExporter`, `IScaraInfoProvider`). Clients depend strictly on the minimal methods they call.
* **D — Dependency Inversion Principle (DIP)**:
  * High-level domain services and CLI executors depend strictly on abstract protocols, never on concrete implementations. All infrastructure dependencies are injected via constructor Dependency Injection (Zero-Fallback DI).

##### Automated Quality Gates (`run_quality_gates.sh`)

Every build is validated against 4 strict automated quality gates:
1. **Structural Protocols Gate (`interfaces_checker.py`)**: Verifies 100% compliance with `@runtime_checkable Protocol` structural typing across concrete implementations.
2. **Interface Segregation Gate (`isp_checker.py`)**: Enforces ISP compliance and verifies that no bloated or unused interfaces exist.
3. **Module Limits Gate (`limits_checker.py`)**: Enforces file length, method count, and line length limits ($\le 150$ characters).
4. **Single Responsibility Gate (`srp_checker.py`)**: Strictly enforces $\le 15$ methods per class and logical method line limits.

#### ✨ Features

* **High-Level SCARA DSL Toolchain**: Lexer, Tokenizer, Line Splitter, AST Parser, Linter, and Semantic Validator for human-readable SCARA motion scripts (`.scara`).
* **Deterministic Bytecode Compiler**: Direct translation of high-level Cartesian DSL trajectories into discrete stepper motor joint step blocks (`JointSteps`, `Step`, `BinaryProgram`).
* **Bidirectional Decompiler**: Full binary-to-source decompilation reconstructing high-level SCARA DSL scripts from compiled bytecode frames (`scarac decompile`).
* **SCARA Binary Wire Protocol Codec**: High-performance streaming frame parser, payload unpacker, frame builder, and CRC-16-CCITT integrity verification (`0xAA 0x55` header framing).
* **Multi-Target Trajectory Exporter**: Export robotic trajectories into industrial G-code, CSV time-series data, JSON trajectory bundles, and SVG vector toolpaths.
* **Interactive Motion REPL Console**: Terminal-based interactive console (`scarac repl`) for real-time single-command compilation, inspection, and frame transmission.
* **Single Source of Truth (SSoT)**: Seamless domain and codec foundation shared between `scarajectory` (Desktop Studio), `scaraemu` (Digital Twin Simulator), and `dof2bot/scara` (RP2040 firmware).
* **Zero GUI Dependencies**: 100% headless, clean architecture design with zero Tkinter, Qt, or graphics dependencies.
* **Strict Quality & SOLID Standards**: 100% structural protocol conformance, 100% test coverage, and 10.00 / 10.00 Pylint score.
* **Resilient Error Handling & Categorized Diagnostics**: Strongly typed domain exception hierarchy (`ScaraSyntaxError`, `ScaraSemanticError`, `ScaraKinematicsError`, `ScaraProtocolError`, `ScaraExportError`, `ScaraIOError`) coupled with dedicated CLI error presentation handlers (`ICompileErrorHandler`, `IDecompileErrorHandler`, `IDisassembleErrorHandler`, `IExportErrorHandler`, `ILintErrorHandler`) providing clear, category-tagged diagnostics (`[SYNTAX]`, `[SEMANTIC]`, `[KINEMATICS]`, `[PROTOCOL]`, `[EXPORT]`, `[IO]`, `[DOMAIN]`) and zero unhandled tracebacks at the system boundary.

#### 📜 SCARA Domain-Specific Language (DSL) & `.scara` Programs

**scaralang** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the `.scara` extension and compiled into validated Cartesian trajectories via a clean AST pipeline:

```
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
                          ScaraCompiler  │ (Macros + Kinematics) 
                                         ▼
                         ┌────────────────────────────┐
                         │       TrajectoryPlan       │
                         |(Waypoints & Discretization)|
                         └───────────────┬────────────┘
                          BinaryCompiler │ (Step Discretization)
                                         ▼
                            ┌─────────────────────────┐
                            │      BinaryProgram      │
                            | (Wire Frames & Bytecode)|
                            └─────────────────────────┘
```

##### SCARA DSL Instruction Quick Reference

> 📖 **Complete Specification:** For the exhaustive parameter reference, boundary checks, linter diagnostics, and full industrial examples, see **[LANGUAGE_REFERENCE.md](LANGUAGE_REFERENCE.md)**.

| Category | Instruction & Syntax | Parameters | Description |
|---|---|---|---|
| **Motion** | `MOVE_J X <x> Y <y> Z <z> [P <phi>]` | `X, Y, Z` (mm), `P` (deg) | Rapid non-interpolated Cartesian joint motion. |
| | `MOVE_L X <x> Y <y> Z <z> [P <phi>]` | `X, Y, Z` (mm), `P` (deg) | Linear continuous path interpolated motion. |
| | `ARC_CW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]` | `X, Y`, `I, J` center offset | Clockwise circular arc interpolation in XY plane. |
| | `ARC_CCW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]` | `X, Y`, `I, J` center offset | Counter-clockwise circular arc interpolation. |
| | `APPROACH DIST <d>` | `DIST` (mm, > 0) | Relative vertical descent along -Z axis. |
| | `RETRACT DIST <d>` | `DIST` (mm, > 0) | Relative vertical ascent along +Z axis. |
| | `JOG_AXIS <X\|Y\|Z\|PHI> <step>` | Axis, step displacement | Incremental single-axis manual jog move. |
| | `JOG_JOINT <1\|2\|3\|4> <deg>` | Joint ID (1..4), angle (deg) | Incremental individual joint rotational jog. |
| | `PROBE [SPEED <s>] [DIST <d>]` | `SPEED` (mm/s), `DIST` (mm) | Tactile surface contact search along -Z axis. |
| **Macros** | `JUMP X <x> Y <y> Z <z> [ARCH <h>]` | `X, Y, Z`, `ARCH` height | 3D parabolic arch pick-and-place transfer. |
| | `PALLET_DEF <id> ROWS <r> COLS <c> DX <dx> DY <dy>`| Matrix dimensions & pitch | Defines structured 2D Cartesian pallet matrix. |
| | `MOVE_PALLET <id> INDEX <i>` | Pallet name, 1-based index | Direct positioning to pallet matrix cell. |
| **Actuators** | `PUMP <ON\|OFF>` | `ON` or `OFF` | Energizes or cuts end-effector vacuum pump. |
| | `VALVE <ON\|OFF>` | `ON` or `OFF` | Opens or closes pneumatic release blow-off valve. |
| | `TOOL <UP\|DOWN>` | `UP` or `DOWN` | Actuates tool head vertical pneumatic slide stage. |
| | `TOOL_ORIENT <AUTO\|TANGENT\|FIXED>` | Tracking mode | Configures 4th-axis tool yaw orientation mode. |
| **Dynamics** | `SPEED <RAPID\|WORK> <val>` | `RAPID` or `WORK`, feedrate | Sets rapid travel or working path feedrate (mm/s). |
| | `ACCEL <val>` | `val` (mm/s²) | Sets trajectory acceleration and deceleration limit. |
| | `OVERRIDE <percent>` | `percent` (10% - 200%) | Dynamically scales path velocity in real time. |
| | `ZONE <OFF\|FINE\|EXACT\|Z1..Z50>` | Blending tolerance (mm) | Corner path rounding and continuous velocity mode. |
| **Kinematics**| `CONFIG ELBOW <LEFT\|RIGHT>` | `LEFT` or `RIGHT` | Sets arm kinematic inverse solution branch. |
| | `CONFIG MOTOR <OPEN_LOOP\|CLOSED_LOOP>`| Drive control mode | Selects open-loop microstepping or closed-loop FOC. |
| | `FRAME X <x> Y <y> Z <z> [PHI <p>]` | Cartesian offsets, angle | Defines local Work Coordinate System (WCS). |
| | `FRAME_RESET` | None | Resets coordinate system to base world origin. |
| | `HOME` | None | Triggers multi-axis hardware homing calibration. |
| **Safety & Flow**| `WAIT <ms>` / `WAIT_MS <ms>` | Duration in milliseconds | Pauses execution dwell for hardware stabilization. |
| | `SYNC` | None | Execution barrier; drains motion queue buffer. |
| | `HOLD` | None | Trajectory feed hold; pauses running motion. |
| | `RESUME` | None | Resumes previously suspended trajectory. |
| | `ESTOP` | None | Immediate emergency stop and motion abort. |
| | `ENABLE` | None | Energizes motor driver stages (holding torque). |
| | `DISABLE` | None | De-energizes motor driver stages (free movement). |

##### Example `.scara` Program: Industrial Pick & Place

```scara
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
```

#### 📡 SCARA Binary Wire Protocol & Codec

All binary wire communication between **scaralang**, **scarajectory**, **scaraemu**, and physical robot firmware is governed by deterministic packet framing:

##### Frame Header & Wire Format

Each binary frame consists of a 4-byte header, variable payload, and 2-byte CRC-16-CCITT checksum:

```
┌──────────────┬──────────────┬──────────────┬──────────────────┬──────────────┐
│  SOF1 (0xAA) │  SOF2 (0x55) │  Msg ID (1B) │  Payload Len (1B)│ Payload (NB) │ ... CRC16 (2B)
└──────────────┴──────────────┴──────────────┴──────────────────┴──────────────┘
```

##### Message Types & Payload Structure

| Message ID | Enum Identifier | Payload Structure | Description |
|---|:---:|---|---|
| `0x01` | `JOINT_STEPS` | `Step[n]` (8 bytes per step: $\Delta S_1, \Delta S_2, \Delta S_3, \Delta S_4$) | Coordinated stepper motor joint step block. |
| `0x02` | `TOOL_COMMAND` | `ToolId (1B), Action (1B), Param (2B)` | End-effector actuator trigger (vacuum, gripper, valve). |
| `0x03` | `ESTOP` | Empty (`0 bytes`) | Immediate hardware emergency stop. |
| `0x04` | `PAUSE` | Empty (`0 bytes`) | Pause execution / feed hold. |
| `0x05` | `RESUME` | Empty (`0 bytes`) | Resume paused trajectory execution. |
| `0x06` | `HEARTBEAT` | `Sequence (4B), Status (1B)` | Real-time link health and operational state beacon. |
| `0x07` | `SYNC` | `Timestamp (4B)` | Clock synchronization and timestamp alignment. |

##### Hardware Execution & Motor Actuation Targets

Binary wire frames generated by **scaralang** stream directly over UART / USB-CDC to the physical **`scara_base`** firmware running on the Raspberry Pi Pico (RP2040), which coordinates motor actuation across two configurable drive modes:
* **Open-Loop Stepper Mode (TMC2209):** Coordinated microstepping pulses generated by RP2040 PIO hardware state machines driving TMC2209 STEP/DIR stages for ultra-silent operation.
* **Closed-Loop Stepper Mode (MKS SERVO42D over CAN Bus):** NEMA stepper motors equipped with **MKS SERVO42D** closed-loop modules communicating with the Raspberry Pi Pico over a high-speed differential **CAN bus** (CAN_H / CAN_L). This guarantees 100% elimination of lost steps, hardware PID closed-loop position correction, and real-time following-error telemetry.

### 🛡️ Error Handling & Diagnostic Architecture

**scaralang** implements end-to-end, resilient error handling and structured diagnostic reporting based on Clean Architecture principles. It enforces a strict separation between domain-level error contracts, core application validation, and presentation-layer error formatting.

#### Domain Exception Hierarchy

All internal toolchain exceptions inherit from the base domain exception `ScaraError` (defined in `scaralang.core.model.exceptions.scara_error`):

```
                                  ┌──────────────┐
                                  │  Exception   │
                                  └──────┬───────┘
                                         ▼
                                  ┌──────────────┐
                                  │  ScaraError  │
                                  └──────┬───────┘
                                         │
        ┌──────────────┬──────────────┬──┴───────────┬──────────────┬──────────────┐
        ▼              ▼              ▼              ▼              ▼              ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐
│ ScaraSyntax  ││ScaraSemantic ││ScaraKinematics│ScaraProtocol ││ ScaraExport  ││  ScaraIO     │
│    Error     ││    Error     ││    Error     ││    Error     ││    Error     ││    Error     │
└──────────────┘└──────────────┘└──────────────┘└──────────────┘└──────────────┘└──────────────┘
```

| Exception Class | Module | Category | Description |
|---|---|:---:|---|
| **`ScaraError`** | `core/model/exceptions/scara_error.py` | `[DOMAIN]` | Base class for all domain, compiler, and protocol exceptions. |
| **`ScaraSyntaxError`** | `core/model/exceptions/scara_syntax_error.py` | `[SYNTAX]` | Lexer, tokenization, or parser grammar violations (e.g., malformed numeric literals, invalid opcodes). |
| **`ScaraSemanticError`** | `core/model/exceptions/scara_semantic_error.py` | `[SEMANTIC]` | Semantic validation failures (e.g., undefined pallet reference, duplicate definitions, missing required parameters). |
| **`ScaraKinematicsError`** | `core/model/exceptions/scara_kinematics_error.py` | `[KINEMATICS]` | Robot workspace, reachability, or mechanical singularity violations (e.g., coordinates exceeding arm reach, deadband violations). |
| **`ScaraProtocolError`** | `core/model/exceptions/scara_protocol_error.py` | `[PROTOCOL]` | Wire framing, CRC-16 checksum failure, invalid message IDs, or truncated payload deserialization faults. |
| **`ScaraExportError`** | `core/model/exceptions/scara_export_error.py` | `[EXPORT]` | Trajectory export format errors, unsupported export targets, or output serialization failures. |
| **`ScaraIOError`** | `core/model/exceptions/scara_io_error.py` | `[IO]` | File system access failures, missing `.scara` or `.bin` input files, or write permission faults. |

#### Dedicated Command Error Handlers

In accordance with the Single Responsibility Principle (SRP) and Interface Segregation Principle (ISP), each CLI subcommand delegates error categorization, return code resolution, and error message formatting to a dedicated error handler component:

| Subcommand | Protocol Interface | Concrete Handler | Companion Factory |
|---|---|---|---|
| **`compile`** | `ICompileErrorHandler` | `CompileErrorHandler` | `CompileErrorHandlerFactory` |
| **`decompile`** | `IDecompileErrorHandler` | `DecompileErrorHandler` | `DecompileErrorHandlerFactory` |
| **`disassemble`** | `IDisassembleErrorHandler` | `DisassembleErrorHandler` | `DisassembleErrorHandlerFactory` |
| **`export`** | `IExportErrorHandler` | `ExportErrorHandler` | `ExportErrorHandlerFactory` |
| **`lint`** | `ILintErrorHandler` | `LintErrorHandler` | `LintErrorHandlerFactory` |

#### Categorized Diagnostics & Formatted Messages

When a command fails, the corresponding error handler captures the domain exception, formats a category-tagged diagnostic message, and sets `returncode = 1` without raw tracebacks:

* **Syntax Errors (`[SYNTAX]`):**
  ```bash
  $ scarac compile --script invalid_syntax.scara
  [SYNTAX] Line 4: Invalid float literal for parameter 'X': '150.abc'
  ```

* **Semantic Errors (`[SEMANTIC]`):**
  ```bash
  $ scarac compile --script invalid_pallet.scara
  [SEMANTIC] Line 12: Referenced pallet 'TRAY1' has not been defined
  ```

* **Kinematics Violations (`[KINEMATICS]`):**
  ```bash
  $ scarac compile --script out_of_reach.scara
  [KINEMATICS] Target coordinates (500.0, 300.0) exceed maximum reach of SCARA arm
  ```

* **Wire Protocol & Deserialization Errors (`[PROTOCOL]`):**
  ```bash
  $ scarac decompile --file corrupted.bin
  [PROTOCOL] Payload truncated: expected 22 bytes for JOINT_STEPS, got 14 bytes
  ```

* **Export Target Errors (`[EXPORT]`):**
  ```bash
  $ scarac export --script program.scara --format unsupported --output out.bin
  [EXPORT] Unsupported export format 'unsupported'
  ```

* **File System / Missing Input Errors (`[IO]`):**
  ```bash
  $ scarac compile --script missing.scara
  compile::execute - file not found: missing.scara
  ```

#### Python Library API: Error Handling Example

Downstream applications (such as `scarajectory` or `scaraemu`) can catch specific domain exceptions for fine-grained recovery:

```python
from scaralang.core.model.exceptions.scara_error import ScaraError
from scaralang.core.model.exceptions.scara_syntax_error import ScaraSyntaxError
from scaralang.core.model.exceptions.scara_semantic_error import ScaraSemanticError
from scaralang.core.model.exceptions.scara_kinematics_error import ScaraKinematicsError
from scaralang.core.service.compiler.dsl.scara_dsl_compiler_factory import ScaraDslCompilerFactory

compiler = ScaraDslCompilerFactory.create_default()

try:
    plan = compiler.compile_script(source="MOVE_J X 999.0 Y 999.0 Z 20.0")
except ScaraSyntaxError as exc:
    print(f"Syntax error in script: {exc}")
except ScaraKinematicsError as exc:
    print(f"Target position violates robot kinematic boundaries: {exc}")
except ScaraSemanticError as exc:
    print(f"Semantic rule violation: {exc}")
except ScaraError as exc:
    print(f"General SCARA domain error: {exc}")
```

### 📊 Code coverage

<details>
<summary><b>Click to expand code coverage</b></summary>

| Name | Stmts | Miss | Cover |
|------|-------|------|-------|
| `scaralang/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/ast/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/ast/command_type.py` | 47 | 0 | 100%|
| `scaralang/core/model/dsl/ast/instruction.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/ast/instruction_param.py` | 57 | 0 | 100%|
| `scaralang/core/model/dsl/ast/jog_axis.py` | 16 | 0 | 100%|
| `scaralang/core/model/dsl/ast/pneumatic_state.py` | 14 | 0 | 100%|
| `scaralang/core/model/dsl/ast/program.py` | 14 | 0 | 100%|
| `scaralang/core/model/dsl/ast/speed_mode.py` | 14 | 0 | 100%|
| `scaralang/core/model/dsl/ast/tool_orient_mode.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/ast/tool_position.py` | 14 | 0 | 100%|
| `scaralang/core/model/dsl/ast/zone_mode.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/binary/axis_peak_steps.py` | 16 | 0 | 100%|
| `scaralang/core/model/dsl/binary/binary_program_telemetry.py` | 19 | 0 | 100%|
| `scaralang/core/model/dsl/binary/disassembled_frame.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/binary/disassembly_summary.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/binary/parsed_command_token.py` | 16 | 0 | 100%|
| `scaralang/core/model/dsl/binary/program.py` | 20 | 0 | 100%|
| `scaralang/core/model/dsl/binary/step.py` | 19 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/arc_geometry.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_blend_state.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_pose_state.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_speed_state.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/control_waypoint_descriptor.py` | 16 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/scara_compiler_context.py` | 27 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic_code.py` | 23 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic_severity.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/exporter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/exporter/export_format.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/linter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/linter/lint_tool_state.py` | 14 | 0 | 100%|
| `scaralang/core/model/dsl/linter/scara_lint_context.py` | 22 | 0 | 100%|
| `scaralang/core/model/dsl/macro/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/macro/pallet_definition.py` | 19 | 0 | 100%|
| `scaralang/core/model/dsl/macro/work_frame.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/token/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/token/lexer_pattern_kind.py` | 22 | 0 | 100%|
| `scaralang/core/model/dsl/token/scara_token.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/token/scara_token_type.py` | 23 | 0 | 100%|
| `scaralang/core/model/exceptions/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_error.py` | 10 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_export_error.py` | 11 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_kinematics_error.py` | 11 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_protocol_error.py` | 11 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_semantic_error.py` | 11 | 0 | 100%|
| `scaralang/core/model/exceptions/scara_syntax_error.py` | 11 | 0 | 100%|
| `scaralang/core/model/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/kinematics/elbow_config.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/joint_angle_bounds.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/link_dimensions.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/point_2d.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/point_3d.py` | 15 | 0 | 100%|
| `scaralang/core/model/kinematics/scara_bounds.py` | 22 | 0 | 100%|
| `scaralang/core/model/kinematics/singularity_margins.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/speed_limits.py` | 17 | 0 | 100%|
| `scaralang/core/model/kinematics/transmission_parameters.py` | 18 | 0 | 100%|
| `scaralang/core/model/kinematics/vertical_bounds.py` | 14 | 0 | 100%|
| `scaralang/core/model/motor/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/motor/axis_mask.py` | 18 | 0 | 100%|
| `scaralang/core/model/motor/motor_config.py` | 18 | 0 | 100%|
| `scaralang/core/model/motor/motor_drive_mode.py` | 14 | 0 | 100%|
| `scaralang/core/model/motor/motor_drive_mode_alias.py` | 14 | 0 | 100%|
| `scaralang/core/model/motor/motor_interface_type.py` | 15 | 0 | 100%|
| `scaralang/core/model/protocol/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/protocol/binary_delimiter.py` | 15 | 0 | 100%|
| `scaralang/core/model/protocol/binary_frame.py` | 17 | 0 | 100%|
| `scaralang/core/model/protocol/error_code.py` | 21 | 0 | 100%|
| `scaralang/core/model/protocol/joint_steps.py` | 18 | 0 | 100%|
| `scaralang/core/model/protocol/message_id.py` | 41 | 0 | 100%|
| `scaralang/core/model/protocol/motor_wire_mode.py` | 14 | 0 | 100%|
| `scaralang/core/model/protocol/tool_id.py` | 13 | 0 | 100%|
| `scaralang/core/model/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/repl/repl_dispatch_result.py` | 15 | 0 | 100%|
| `scaralang/core/model/repl/repl_pose_state.py` | 16 | 0 | 100%|
| `scaralang/core/model/repl/repl_session_context.py` | 21 | 0 | 100%|
| `scaralang/core/model/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/trajectory/arc_point.py` | 15 | 0 | 100%|
| `scaralang/core/model/trajectory/axis_peak_metric.py` | 16 | 0 | 100%|
| `scaralang/core/model/trajectory/bottleneck_incident.py` | 16 | 0 | 100%|
| `scaralang/core/model/trajectory/circle_geometry.py` | 18 | 0 | 100%|
| `scaralang/core/model/trajectory/trajectory_cycle_report.py` | 18 | 0 | 100%|
| `scaralang/core/model/trajectory/validation_result.py` | 15 | 0 | 100%|
| `scaralang/core/model/trajectory/waypoint.py` | 19 | 0 | 100%|
| `scaralang/core/service/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/binary_compiler.py` | 30 | 0 | 100%|
| `scaralang/core/service/compiler/binary/binary_compiler_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/command_compiler.py` | 59 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/command_compiler_factory.py` | 31 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/icommand_compiler.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/motor/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/motor/imotor_frame_builder.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/motor/motor_frame_builder.py` | 25 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/motor/motor_frame_builder_factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/command_token_parser.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/command_token_parser_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/icommand_token_parser.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/itool_frame_builder.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/tool_frame_builder.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/tool_frame_builder_factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/ibinary_compiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/binary_metrics_calculator.py` | 27 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/binary_metrics_calculator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/ibinary_metrics_calculator.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/imotion_compiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/motion_compiler.py` | 30 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/motion_compiler_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/istep_discretizer.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/iwaypoint_step_dispatcher.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/step_discretizer.py` | 43 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/step_discretizer_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/waypoint_step_dispatcher.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/waypoint_step_dispatcher_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/iscara_dsl_binary_compiler.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/iscara_dsl_compiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/scara_dsl_binary_compiler.py` | 31 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/scara_dsl_binary_compiler_factory.py` | 24 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/scara_dsl_compiler.py` | 42 | 0 | 100%|
| `scaralang/core/service/compiler/dsl/scara_dsl_compiler_factory.py` | 37 | 0 | 100%|
| `scaralang/core/service/compiler/iinstruction_pipeline.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/instruction_pipeline.py` | 38 | 0 | 100%|
| `scaralang/core/service/compiler/instruction_pipeline_factory.py` | 27 | 0 | 100%|
| `scaralang/core/service/compiler/iprimitive_instruction_processor.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/iscara_compiler.py` | 22 | 0 | 100%|
| `scaralang/core/service/compiler/macro/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/frame_macro_expander.py` | 29 | 0 | 100%|
| `scaralang/core/service/compiler/macro/frame_macro_expander_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/macro/imacro_expander.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/macro/itangent_macro_expander.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/macro/jump_macro_expander.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/macro/jump_macro_expander_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet_macro_expander.py` | 51 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet_macro_expander_factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/macro/tangent_macro_expander.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/macro/tangent_macro_expander_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/arc_move_compiler.py` | 40 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/arc_move_compiler_factory.py` | 29 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/builder/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/builder/arc_waypoint_builder.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/builder/arc_waypoint_builder_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/builder/iarc_waypoint_builder.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/calculator/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/calculator/arc_point_calculator.py` | 37 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/calculator/arc_point_calculator_factory.py` | 28 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/calculator/iarc_point_calculator.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/interpolation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/interpolation/arc_interpolator.py` | 43 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/interpolation/arc_interpolator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/motion/arc/interpolation/iarc_interpolator.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/motion/cartesian/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/cartesian/cartesian_move_compiler.py` | 45 | 0 | 100%|
| `scaralang/core/service/compiler/motion/cartesian/cartesian_move_compiler_factory.py` | 28 | 0 | 100%|
| `scaralang/core/service/compiler/motion/imotion_sub_compiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/motion/motion_command_compiler.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/motion/motion_command_compiler_factory.py` | 26 | 0 | 100%|
| `scaralang/core/service/compiler/motion/vertical/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/motion/vertical/vertical_move_compiler.py` | 32 | 0 | 100%|
| `scaralang/core/service/compiler/motion/vertical/vertical_move_compiler_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/plan/itrajectory_plan_compiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/plan/trajectory_plan_compiler.py` | 35 | 0 | 100%|
| `scaralang/core/service/compiler/plan/trajectory_plan_compiler_factory.py` | 43 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/control_command_compiler.py` | 42 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/control_command_compiler_factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/control_waypoint_builder.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/control_waypoint_builder_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/icontrol_waypoint_builder.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/iprimitive_compiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/state_command_compiler.py` | 46 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/state_command_compiler_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/itool_waypoint_builder.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/tool_command_compiler.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/tool_command_compiler_factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/tool_waypoint_builder.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/tool_waypoint_builder_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive_instruction_processor.py` | 27 | 0 | 100%|
| `scaralang/core/service/compiler/primitive_instruction_processor_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/scara_compiler.py` | 37 | 0 | 100%|
| `scaralang/core/service/compiler/scara_compiler_factory.py` | 44 | 0 | 100%|
| `scaralang/core/service/decompiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/decompiler/frame_decompiler.py` | 67 | 0 | 100%|
| `scaralang/core/service/decompiler/frame_decompiler_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/decompiler/iframe_decompiler.py` | 15 | 0 | 100%|
| `scaralang/core/service/decompiler/iscara_decompiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/decompiler/scara_decompiler.py` | 37 | 0 | 100%|
| `scaralang/core/service/decompiler/scara_decompiler_factory.py` | 34 | 0 | 100%|
| `scaralang/core/service/disassembler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/disassembler/frame_detail_decoder.py` | 63 | 0 | 100%|
| `scaralang/core/service/disassembler/frame_detail_decoder_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/disassembler/iframe_detail_decoder.py` | 15 | 0 | 100%|
| `scaralang/core/service/disassembler/iscara_disassembler.py` | 19 | 0 | 100%|
| `scaralang/core/service/disassembler/scara_disassembler.py` | 35 | 0 | 100%|
| `scaralang/core/service/disassembler/scara_disassembler_factory.py` | 29 | 0 | 100%|
| `scaralang/core/service/exporter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/csv/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/csv/csv_trajectory_exporter.py` | 19 | 0 | 100%|
| `scaralang/core/service/exporter/csv/csv_trajectory_exporter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/csv/icsv_trajectory_exporter.py` | 16 | 0 | 100%|
| `scaralang/core/service/exporter/export_dispatcher_bundle.py` | 22 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/gcode_exporter.py` | 24 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/gcode_exporter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/igcode_exporter.py` | 16 | 0 | 100%|
| `scaralang/core/service/exporter/iscara_exporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/json/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/json/ijson_trajectory_exporter.py` | 16 | 0 | 100%|
| `scaralang/core/service/exporter/json/json_trajectory_exporter.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/json/json_trajectory_exporter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/scara/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/scara/iscara_plan_exporter.py` | 16 | 0 | 100%|
| `scaralang/core/service/exporter/scara/scara_plan_exporter.py` | 27 | 0 | 100%|
| `scaralang/core/service/exporter/scara/scara_plan_exporter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/scara/scara_program_serializer.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/scara/scara_source_generator.py` | 22 | 0 | 100%|
| `scaralang/core/service/exporter/scara_exporter.py` | 49 | 0 | 100%|
| `scaralang/core/service/exporter/scara_exporter_factory.py` | 28 | 0 | 100%|
| `scaralang/core/service/exporter/svg/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/svg/isvg_trajectory_exporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/svg/svg_trajectory_exporter.py` | 25 | 0 | 100%|
| `scaralang/core/service/exporter/svg/svg_trajectory_exporter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/info/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/info/iscara_info_provider.py` | 17 | 0 | 100%|
| `scaralang/core/service/info/scara_info_provider.py` | 46 | 0 | 100%|
| `scaralang/core/service/info/scara_info_provider_factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/default_scara_profile.py` | 26 | 0 | 100%|
| `scaralang/core/service/kinematics/ikinematics_service.py` | 26 | 0 | 100%|
| `scaralang/core/service/kinematics/kinematics_service.py` | 96 | 0 | 100%|
| `scaralang/core/service/kinematics/kinematics_service_factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/ijoint_step_transmission_converter.py` | 16 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/joint_step_transmission_converter.py` | 32 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/joint_step_transmission_converter_factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/linter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/iscara_diagnostic_formatter.py` | 15 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/scara_diagnostic_formatter.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/scara_diagnostic_formatter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/iscara_linter.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/iscara_lint_rule.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/imotion_calibration_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/imotion_duplicate_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_calibration_validator.py` | 22 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_calibration_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_duplicate_validator.py` | 39 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_duplicate_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_lint_rule.py` | 34 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/motion_lint_rule_factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/ipneumatic_conflict_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/ipneumatic_flyby_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/ipneumatic_redundancy_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_conflict_validator.py` | 32 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_conflict_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_flyby_validator.py` | 25 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_flyby_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_lint_rule.py` | 45 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_lint_rule_factory.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_redundancy_validator.py` | 32 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/pneumatic_redundancy_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/imotor_mode_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/istate_homing_validator.py` | 17 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/istate_zone_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/motor_mode_validator.py` | 35 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/motor_mode_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_homing_validator.py` | 20 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_homing_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_lint_rule.py` | 38 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_lint_rule_factory.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_zone_validator.py` | 37 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/state_zone_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/itiming_blend_zone_validator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/itiming_dwell_validator.py` | 17 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_blend_zone_validator.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_blend_zone_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_dwell_validator.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_dwell_validator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_lint_rule.py` | 33 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/timing_lint_rule_factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/linter/scara_linter.py` | 35 | 0 | 100%|
| `scaralang/core/service/linter/scara_linter_factory.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/script/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/script/iscara_dsl_linter.py` | 15 | 0 | 100%|
| `scaralang/core/service/linter/script/iscara_dsl_validator.py` | 16 | 0 | 100%|
| `scaralang/core/service/linter/script/scara_script_validator.py` | 56 | 0 | 100%|
| `scaralang/core/service/linter/script/scara_script_validator_factory.py` | 37 | 0 | 100%|
| `scaralang/core/service/motor/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/motor/motor_config_factory.py` | 51 | 0 | 100%|
| `scaralang/core/service/motor/motor_drive_mode_resolver.py` | 31 | 0 | 100%|
| `scaralang/core/service/motor/motor_interface_resolver.py` | 31 | 0 | 100%|
| `scaralang/core/service/motor/motor_wire_mode_converter.py` | 25 | 0 | 100%|
| `scaralang/core/service/parser/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/accel_config_parser.py` | 30 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/config_command_parser_factory.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/elbow_config_parser.py` | 33 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/motor_config_parser.py` | 58 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/override_config_parser.py` | 30 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/speed_config_parser.py` | 34 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/tool_orient_command_parser.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/zone_command_parser.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/disable_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/enable_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/estop_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/flow_command_parser_factory.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/hold_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/resume_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/sync_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/wait_command_parser.py` | 32 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/frame_command_parser_factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/frame_reset_command_parser.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/frame_set_command_parser.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/icommand_parser.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/commands/icommand_parser_provider.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/jump_command_parser.py` | 27 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/macro_command_parser_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/pallet_def_command_parser.py` | 31 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/pallet_move_command_parser.py` | 31 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/approach_command_parser.py` | 22 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/arc_command_parser.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/home_command_parser.py` | 21 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/jog_command_parser.py` | 42 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/joint_move_command_parser.py` | 22 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/linear_move_command_parser.py` | 22 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/motion_command_parser_factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/probe_command_parser.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/retract_command_parser.py` | 22 | 0 | 100%|
| `scaralang/core/service/parser/commands/parameter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/parameter/parameter_extractor.py` | 39 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/pump_command_parser.py` | 32 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/tool_command_parser.py` | 32 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/tool_command_parser_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/valve_command_parser.py` | 32 | 0 | 100%|
| `scaralang/core/service/parser/instruction/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/instruction/iinstruction_line_parser.py` | 20 | 0 | 100%|
| `scaralang/core/service/parser/instruction/instruction_line_parser.py` | 55 | 0 | 100%|
| `scaralang/core/service/parser/instruction/instruction_line_parser_factory.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/iscara_parser.py` | 19 | 0 | 100%|
| `scaralang/core/service/parser/lexer/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/lexer/iscara_lexer.py` | 16 | 0 | 100%|
| `scaralang/core/service/parser/lexer/scara_lexer.py` | 45 | 0 | 100%|
| `scaralang/core/service/parser/lexer/scara_lexer_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/scara_parser.py` | 34 | 0 | 100%|
| `scaralang/core/service/parser/scara_parser_factory.py` | 31 | 0 | 100%|
| `scaralang/core/service/parser/splitter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/splitter/itoken_line_splitter.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/splitter/token_line_splitter.py` | 28 | 0 | 100%|
| `scaralang/core/service/parser/splitter/token_line_splitter_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/protocol/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_frame_builder.py` | 25 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_frame_parser.py` | 18 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_payload_unpacker.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/ishape_discretizer.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/shape_discretizer.py` | 39 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/shape_discretizer_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/imotion_bottleneck_detector.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/motion_bottleneck_detector.py` | 33 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/motion_bottleneck_detector_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/cycle_time_calculator.py` | 40 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/cycle_time_calculator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/icycle_time_calculator.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/axis_speed_profile_analyzer.py` | 45 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/axis_speed_profile_analyzer_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/iaxis_speed_profile_analyzer.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/itrajectory_cycle_summary_builder.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/trajectory_cycle_summary_builder.py` | 35 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/trajectory_cycle_summary_builder_factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/trajectory_metrics.py` | 40 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/itrajectory_mutable.py` | 21 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/itrajectory_plan.py` | 13 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/itrajectory_plan_factory.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/itrajectory_read_only.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/trajectory_plan.py` | 42 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/trajectory_plan_factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/feedrate_validator.py` | 25 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/feedrate_validator_factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/ifeedrate_validator.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/itrajectory_validator.py` | 28 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/itrajectory_plan_validator.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/trajectory_plan_validator.py` | 44 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/trajectory_plan_validator_factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/trajectory_validator.py` | 46 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/trajectory_validator_factory.py` | 28 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/iwaypoint_validator.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/waypoint_validator.py` | 33 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/waypoint_validator_factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/transformation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/transformation/frame_transformer.py` | 24 | 0 | 100%|
| `scaralang/core/service/transformation/frame_transformer_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/transformation/iframe_transformer.py` | 16 | 0 | 100%|
| `scaralang/engine.py` | 60 | 0 | 100%|
| `scaralang/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/engine.py` | 43 | 0 | 100%|
| `scaralang/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/irepl_single_command_compiler.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/repl_single_command_compiler.py` | 51 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/repl_single_command_compiler_factory.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/dispatch/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/dispatch/irepl_command_dispatcher.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/dispatch/repl_command_dispatcher.py` | 50 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/dispatch/repl_command_dispatcher_factory.py` | 22 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/input/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/input/irepl_line_reader.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/input/repl_line_reader.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/input/repl_line_reader_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/output/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/output/irepl_output_writer.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/output/repl_output_writer.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/output/repl_output_writer_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/presentation/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/presentation/irepl_response_presenter.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/presentation/repl_response_presenter.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/presentation/repl_response_presenter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/transmission/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/transmission/irepl_frame_transmitter.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/transmission/repl_frame_transmitter.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/transmission/repl_frame_transmitter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/bundle.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/dep_validator.py` | 37 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/dependencies.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/factory.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/keys.py` | 23 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/opt_validator.py` | 35 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/options.py` | 13 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/registry.py` | 29 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/validator.py` | 38 | 0 | 100%|
| `scaralang/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/command_bundle.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/command_bundle_factory.py` | 31 | 0 | 100%|
| `scaralang/infrastructure/command/compile/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/bundle.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/compile/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/compile_error_handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/compile_error_handler_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/icompile_error_handler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/executor.py` | 60 | 0 | 100%|
| `scaralang/infrastructure/command/compile/executor_factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/frame_header_formatter.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/frame_header_formatter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/frame_trailer_formatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/frame_trailer_formatter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/hex_stream_formatter.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/hex_stream_formatter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/iframe_header_formatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/iframe_trailer_formatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/ihex_stream_formatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/ijoint_steps_payload_formatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/ipayload_dispatcher_formatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/itool_command_payload_formatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint_steps_payload_formatter.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint_steps_payload_formatter_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/payload_dispatcher_formatter.py` | 45 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/payload_dispatcher_formatter_factory.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool_command_payload_formatter.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool_command_payload_formatter_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/frame_step_presenter.py` | 36 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/frame_step_presenter_factory.py` | 21 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/iframe_step_presenter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/iprogram_inspection_presenter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program_inspection_presenter.py` | 27 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program_inspection_presenter_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/compile_telemetry_formatter.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/compile_telemetry_formatter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/icompile_telemetry_formatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/decompile_error_handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/decompile_error_handler_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/idecompile_error_handler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/executor.py` | 44 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/executor_factory.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/disassemble_error_handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/disassemble_error_handler_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/idisassemble_error_handler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/executor.py` | 55 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/executor_factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/disassemble_summary_formatter.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/disassemble_summary_formatter_factory.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/idisassemble_summary_formatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/export/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/export/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/export_error_handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/export_error_handler_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/iexport_error_handler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/export/executor.py` | 52 | 0 | 100%|
| `scaralang/infrastructure/command/export/executor_factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/command/icommand_definition.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/icommand_executor.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/info/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/info/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/info/executor.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/command/info/executor_factory.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/lint/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/lint/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/ilint_error_handler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/lint_error_handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/lint_error_handler_factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/lint/executor.py` | 46 | 0 | 100%|
| `scaralang/infrastructure/command/lint/executor_factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/command/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/repl/bundle.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/repl/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/repl/executor.py` | 83 | 0 | 100%|
| `scaralang/infrastructure/command/repl/executor_factory.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/communication/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/binary_struct_format.py` | 23 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/builder/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/builder/binary_frame_builder.py` | 56 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/builder/binary_frame_builder_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/checksum/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/checksum/crc16_ccitt.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_frame_assembler.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_frame_assembler_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_frame_parser.py` | 91 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_frame_parser_factory.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_payload_unpacker.py` | 56 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/binary_payload_unpacker_factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/ibinary_frame_assembler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/communication/protocol/binary/parser/parser_state.py` | 20 | 0 | 100%|
| `scaralang/setup/__init__.py` | 9 | 0 | 100%|
| `scaralang/setup/bundle.py` | 19 | 0 | 100%|
| `scaralang/setup/dep_validator.py` | 36 | 0 | 100%|
| `scaralang/setup/dependencies.py` | 15 | 0 | 100%|
| `scaralang/setup/factory.py` | 38 | 0 | 100%|
| `scaralang/setup/keys.py` | 24 | 0 | 100%|
| `scaralang/setup/opt_validator.py` | 34 | 0 | 100%|
| `scaralang/setup/options.py` | 13 | 0 | 100%|
| `scaralang/setup/registry.py` | 28 | 0 | 100%|
| `scaralang/setup/validator.py` | 38 | 0 | 100%|
| **Total** | 12624 | 0 | 100% |

</details>

### 🛠 Usage

##### CLI Tool (`scarac` / `scaralang`)

```bash
# Display general help and available subcommands
scarac --help

# Validate syntax and run static diagnostic lint checks
scarac lint --script program.scara

# Compile DSL program to packed binary execution file (.bin)
scarac compile --script program.scara --output program.bin

# Compile with hexadecimal stream output and detailed wire frame breakdown
scarac compile --script program.scara --hex --dump-frames --verbose

# Decompile binary bytecode file (.bin) back into high-level SCARA DSL script
scarac decompile --file program.bin --output decompiled.scara

# Disassemble binary bytecode file into human-readable frame breakdown
scarac disassemble --file program.bin --summary

# Export trajectory to industrial G-code, CSV time-series, JSON, SVG, or SCARA
scarac export --script program.scara --format gcode --output program.gcode
scarac export --script program.scara --format csv --output trajectory.csv
scarac export --script program.scara --format json --output trajectory.json
scarac export --script program.scara --format svg --output toolpath.svg

# Inspect toolchain info, supported commands, and grammar version
scarac info --verbose

# Launch interactive SCARA DSL motion REPL console
scarac repl --endpoint dry-run
```

##### CLI Subcommand Reference

| Subcommand | Description | Key Options |
|---|---|---|
| **`lint`** | Validate syntax and static analysis rules of a .scara DSL script. | `--script` |
| **`compile`** | Compile a .scara DSL script into binary wire frames and packets. | `--script`, `--output`, `--hex`, `--dump-frames`, `--verbose` |
| **`decompile`** | Decompile binary frames from a .bin file into high-level SCARA DSL script. | `--file`, `--output` |
| **`disassemble`** | Decode binary frames from a .bin file into human-readable instructions. | `--file`, `--summary` |
| **`export`** | Export trajectory plan to multi-target formats (G-code, CSV, JSON, SVG, SCARA). | `--script`, `--format <gcode\|csv\|json\|svg\|scara>`, `--output` |
| **`info`** | Display compiler version, supported grammar, and binary protocol specifications. | `--verbose` |
| **`repl`** | Interactive terminal REPL motion console for single-line execution. | `--endpoint`, `--dry-run` |

##### Python Library API

```python
from scaralang.core.service.compiler.dsl.scara_dsl_compiler_factory import ScaraDslCompilerFactory
from scaralang.core.service.compiler.dsl.scara_dsl_binary_compiler_factory import ScaraDslBinaryCompilerFactory
from scaralang.core.service.linter.script.scara_script_validator_factory import ScaraScriptValidatorFactory
from scaralang.core.service.decompiler.scara_decompiler_factory import ScaraDecompilerFactory

# Initialize fine-grained role services via their factories
validator = ScaraScriptValidatorFactory.create_default()
compiler = ScaraDslCompilerFactory.create_default()
binary_compiler = ScaraDslBinaryCompilerFactory.create_default()
decompiler = ScaraDecompilerFactory.create_default()

# SCARA DSL script to analyze and compile
script = """HOME
SPEED RAPID 100.0
MOVE_J X 150.0 Y 50.0 Z 20.0
PUMP ON
WAIT 100
MOVE_L X 180.0 Y 50.0 Z 20.0
PUMP OFF
"""

# 1. Validate syntax and kinematics
is_valid, diagnostics = validator.validate_script(source=script)
if is_valid:
    # 2. Compile into validated trajectory plan
    plan = compiler.compile_script(source=script)
    print(f"Trajectory plan contains {len(plan.waypoints)} waypoints.")

    # 3. Compile directly to binary program package and raw bytecode
    binary_prog = binary_compiler.compile_to_binary(source=script)
    raw_bytes = binary_compiler.compile_to_bytes(source=script)
    telemetry = binary_compiler.get_program_telemetry(program=binary_prog)
    print(f"Generated {len(raw_bytes)} bytes of binary bytecode.")
    print(f"Total motor steps: {len(binary_prog.steps)}")
    print(f"Trajectory execution time: {telemetry.duration_s:.2f} s")

    # 4. Decompile binary bytecode back into high-level SCARA DSL script
    decompiled_script = decompiler.decompile_bytes(data=raw_bytes)
    print("Decompiled script:")
    print(decompiled_script)
```

### 📚 Docs

[![Documentation Status](https://readthedocs.org/projects/scaralang/badge/?version=latest)](https://scaralang.readthedocs.io/en/latest/?badge=latest)

More documentation and info at

* [scaralang.readthedocs.io](https://scaralang.readthedocs.io)
* [www.python.org](https://www.python.org/)

### 👥 Contributing

[Contributing to scaralang](CONTRIBUTING.md)

### 📄 Copyright and licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2026 by [vroncevic.github.io/scaralang](https://vroncevic.github.io/scaralang)

**scaralang** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 3.x or,
at your option, any later version of Python 3 you may have available.

Special thanks to **Google** and the Google developer ecosystem for their tremendous support and innovative tools from the Google bundle that empowered the development and realization of this project. *Google, you make this world a better place!* 🌍✨

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/scaralang/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.python.org/psf/donations/)
