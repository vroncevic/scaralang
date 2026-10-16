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
    - [Dead Zone Avoidance & Safe Trajectory Routing Pipeline](#dead-zone-avoidance--safe-trajectory-routing-pipeline)
    - [SCARA DSL Instruction Quick Reference](#scara-dsl-instruction-quick-reference)
    - [Example `.scara` Program: Industrial Pick & Place](#example-scara-program-industrial-pick--place)
    - [📁 Verification Scripts & Examples (`examples/` & `run.sh`)](#-verification-scripts--examples-examples--runsh)
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
         │   │   │   │   ├── compiler_context.py
         │   │   │   │   ├── compiler_pose_state.py
         │   │   │   │   ├── compiler_speed_state.py
         │   │   │   │   ├── control_waypoint_descriptor.py
         │   │   │   │   └── __init__.py
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
         │   │   │   │   ├── lint_context.py
         │   │   │   │   └── lint_tool_state.py
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
         │   │   │   ├── axis_name.py
         │   │   │   ├── cartesian_pose.py
         │   │   │   ├── elbow_config.py
         │   │   │   ├── ik_status.py
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_angle_bounds.py
         │   │   │   ├── joint_angles.py
         │   │   │   ├── joint_step_coordinates.py
         │   │   │   ├── link_dimensions.py
         │   │   │   ├── point_2d.py
         │   │   │   ├── point_3d.py
         │   │   │   ├── scara_bounds.py
         │   │   │   ├── scara_joints.py
         │   │   │   ├── scara_joints_2d.py
         │   │   │   ├── scara_joints_3d.py
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
         │   │   │   ├── binary_payload_size.py
         │   │   │   ├── error_code.py
         │   │   │   ├── __init__.py
         │   │   │   ├── joint_steps.py
         │   │   │   ├── manipulator_status.py
         │   │   │   ├── message_id.py
         │   │   │   ├── motor_wire_mode.py
         │   │   │   ├── move_event_type.py
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
         │   │       ├── bypass_arc_geometry.py
         │   │       ├── circle_geometry.py
         │   │       ├── constraint_type.py
         │   │       ├── __init__.py
         │   │       ├── trajectory_cycle_report.py
         │   │       ├── validation_result.py
         │   │       └── waypoint.py
         │   └── service/
         │       ├── compiler/
         │       │   ├── binary/
         │       │   │   ├── command/
         │       │   │   │   ├── actuator/
         │       │   │   │   │   ├── builder.py
         │       │   │   │   │   ├── dependencies.py
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── ibuilder.py
         │       │   │   │   │   └── __init__.py
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── compiler_dependencies.py
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icompiler.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── tokens/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── iparser.py
         │       │   │   │   │   └── parser.py
         │       │   │   │   └── tool/
         │       │   │   │       ├── builder.py
         │       │   │   │       ├── dependencies.py
         │       │   │   │       ├── factory.py
         │       │   │   │       ├── ibuilder.py
         │       │   │   │       └── __init__.py
         │       │   │   ├── compiler.py
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── icompiler.py
         │       │   │   ├── __init__.py
         │       │   │   ├── metrics/
         │       │   │   │   ├── calculator.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icalculator.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── motion/
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icompiler.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── provides.py
         │       │   │   ├── provides.py
         │       │   │   └── step/
         │       │   │       ├── discretizer/
         │       │   │       │   ├── dependencies.py
         │       │   │       │   ├── discretizer.py
         │       │   │       │   ├── factory.py
         │       │   │       │   ├── idiscretizer.py
         │       │   │       │   └── __init__.py
         │       │   │       ├── dispatcher/
         │       │   │       │   ├── dependencies.py
         │       │   │       │   ├── dispatcher.py
         │       │   │       │   ├── factory.py
         │       │   │       │   ├── idispatcher.py
         │       │   │       │   └── __init__.py
         │       │   │       ├── duration/
         │       │   │       │   ├── calculator.py
         │       │   │       │   ├── factory.py
         │       │   │       │   ├── icalculator.py
         │       │   │       │   └── __init__.py
         │       │   │       └── __init__.py
         │       │   ├── compiler.py
         │       │   ├── context/
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── icompiler.py
         │       │   ├── __init__.py
         │       │   ├── instruction/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── __init__.py
         │       │   │   ├── pipeline/
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── ipipeline.py
         │       │   │   │   └── pipeline.py
         │       │   │   ├── processor/
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── iprocessor.py
         │       │   │   │   └── processor.py
         │       │   │   └── provides.py
         │       │   ├── macro/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── frame/
         │       │   │   │   ├── expander.py
         │       │   │   │   ├── factory.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── iexpander.py
         │       │   │   ├── __init__.py
         │       │   │   ├── jump/
         │       │   │   │   ├── expander.py
         │       │   │   │   ├── factory.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── pallet/
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── expander.py
         │       │   │   │   ├── factory.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── provides.py
         │       │   │   └── tangent/
         │       │   │       ├── expander.py
         │       │   │       ├── factory.py
         │       │   │       └── __init__.py
         │       │   ├── plan/
         │       │   │   ├── ast/
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icompiler.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── __init__.py
         │       │   │   ├── provides.py
         │       │   │   └── script/
         │       │   │       ├── compiler.py
         │       │   │       ├── dependencies.py
         │       │   │       ├── factory.py
         │       │   │       ├── icompiler.py
         │       │   │       └── __init__.py
         │       │   ├── primitive/
         │       │   │   ├── control/
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── waypoint/
         │       │   │   │       ├── builder.py
         │       │   │   │       ├── factory.py
         │       │   │   │       ├── ibuilder.py
         │       │   │   │       └── __init__.py
         │       │   │   ├── factory.py
         │       │   │   ├── icompiler.py
         │       │   │   ├── __init__.py
         │       │   │   ├── motion/
         │       │   │   │   ├── arc/
         │       │   │   │   │   ├── calculator/
         │       │   │   │   │   │   ├── calculator.py
         │       │   │   │   │   │   ├── factory.py
         │       │   │   │   │   │   ├── icalculator.py
         │       │   │   │   │   │   └── __init__.py
         │       │   │   │   │   ├── compiler.py
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── interpolation/
         │       │   │   │   │   │   ├── factory.py
         │       │   │   │   │   │   ├── iinterpolator.py
         │       │   │   │   │   │   ├── __init__.py
         │       │   │   │   │   │   └── interpolator.py
         │       │   │   │   │   └── waypoint/
         │       │   │   │   │       ├── builder.py
         │       │   │   │   │       ├── factory.py
         │       │   │   │   │       ├── ibuilder.py
         │       │   │   │   │       └── __init__.py
         │       │   │   │   ├── cartesian/
         │       │   │   │   │   ├── compiler.py
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── itangent_heading_calculator.py
         │       │   │   │   │   ├── tangent_heading_calculator.py
         │       │   │   │   │   └── tangent_heading_calculator_factory.py
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── isub_compiler.py
         │       │   │   │   └── vertical/
         │       │   │   │       ├── compiler.py
         │       │   │   │       ├── factory.py
         │       │   │   │       └── __init__.py
         │       │   │   ├── provides.py
         │       │   │   ├── state/
         │       │   │   │   ├── compiler.py
         │       │   │   │   ├── factory.py
         │       │   │   │   └── __init__.py
         │       │   │   └── tool/
         │       │   │       ├── compiler.py
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       └── waypoint/
         │       │   │           ├── builder.py
         │       │   │           ├── factory.py
         │       │   │           ├── ibuilder.py
         │       │   │           └── __init__.py
         │       │   └── provides.py
         │       ├── decompiler/
         │       │   ├── decompiler.py
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── frame/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── frame.py
         │       │   │   ├── iframe.py
         │       │   │   ├── __init__.py
         │       │   │   └── provides.py
         │       │   ├── idecompiler.py
         │       │   ├── __init__.py
         │       │   └── provides.py
         │       ├── disassembler/
         │       │   ├── dependencies.py
         │       │   ├── disassembler.py
         │       │   ├── factory.py
         │       │   ├── frame/
         │       │   │   ├── decoder/
         │       │   │   │   ├── actuator_decoder.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── idecoder.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── joint_steps_decoder.py
         │       │   │   │   └── system_decoder.py
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── frame.py
         │       │   │   ├── iframe.py
         │       │   │   ├── __init__.py
         │       │   │   └── provides.py
         │       │   ├── idisassembler.py
         │       │   ├── __init__.py
         │       │   └── provides.py
         │       ├── exporter/
         │       │   ├── csv/
         │       │   │   ├── exporter.py
         │       │   │   ├── factory.py
         │       │   │   ├── iexporter.py
         │       │   │   └── __init__.py
         │       │   ├── dependencies.py
         │       │   ├── exporter.py
         │       │   ├── factory.py
         │       │   ├── gcode/
         │       │   │   ├── exporter.py
         │       │   │   ├── factory.py
         │       │   │   ├── iexporter.py
         │       │   │   └── __init__.py
         │       │   ├── iexporter.py
         │       │   ├── __init__.py
         │       │   ├── json/
         │       │   │   ├── exporter.py
         │       │   │   ├── factory.py
         │       │   │   ├── iexporter.py
         │       │   │   └── __init__.py
         │       │   ├── provides.py
         │       │   ├── scara/
         │       │   │   ├── exporter.py
         │       │   │   ├── factory.py
         │       │   │   ├── formatter/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── formatter.py
         │       │   │   │   ├── iformatter.py
         │       │   │   │   └── __init__.py
         │       │   │   ├── iexporter.py
         │       │   │   ├── __init__.py
         │       │   │   ├── serializer.py
         │       │   │   └── source_generator.py
         │       │   └── svg/
         │       │       ├── exporter.py
         │       │       ├── factory.py
         │       │       ├── iexporter.py
         │       │       └── __init__.py
         │       ├── info/
         │       │   ├── factory.py
         │       │   ├── iinfo.py
         │       │   ├── info.py
         │       │   ├── __init__.py
         │       │   └── provides.py
         │       ├── __init__.py
         │       ├── kinematics/
         │       │   ├── dependencies.py
         │       │   ├── envelope/
         │       │   │   ├── envelope.py
         │       │   │   ├── factory.py
         │       │   │   ├── ienvelope.py
         │       │   │   └── __init__.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── profile/
         │       │   │   ├── default_scara_profile.py
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   ├── provides.py
         │       │   ├── solver/
         │       │   │   ├── __init__.py
         │       │   │   ├── planar/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── isolver.py
         │       │   │   │   └── solver.py
         │       │   │   └── spatial/
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       ├── isolver.py
         │       │   │       └── solver.py
         │       │   ├── transmission/
         │       │   │   ├── converter.py
         │       │   │   ├── factory.py
         │       │   │   ├── iconverter.py
         │       │   │   └── __init__.py
         │       │   └── workspace/
         │       │       ├── boundary/
         │       │       │   ├── factory.py
         │       │       │   ├── __init__.py
         │       │       │   ├── iservice.py
         │       │       │   ├── provides.py
         │       │       │   └── service.py
         │       │       ├── evaluator.py
         │       │       ├── factory.py
         │       │       ├── ievaluator.py
         │       │       └── __init__.py
         │       ├── linter/
         │       │   ├── context/
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   ├── diagnostic/
         │       │   │   ├── factory.py
         │       │   │   ├── formatter.py
         │       │   │   ├── iformatter.py
         │       │   │   ├── __init__.py
         │       │   │   └── provides.py
         │       │   ├── factory.py
         │       │   ├── ilinter.py
         │       │   ├── __init__.py
         │       │   ├── linter.py
         │       │   ├── provides.py
         │       │   ├── rules/
         │       │   │   ├── __init__.py
         │       │   │   ├── irule.py
         │       │   │   ├── motion/
         │       │   │   │   ├── calibration/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── duplicate/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── provides.py
         │       │   │   │   └── rule.py
         │       │   │   ├── pneumatic/
         │       │   │   │   ├── conflict/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── flyby/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── redundancy/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   └── rule.py
         │       │   │   ├── state/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── homing/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── mode/
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── ivalidator.py
         │       │   │   │   │   └── validator.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── rule.py
         │       │   │   │   └── zone/
         │       │   │   │       ├── factory.py
         │       │   │   │       ├── __init__.py
         │       │   │   │       ├── ivalidator.py
         │       │   │   │       └── validator.py
         │       │   │   └── timing/
         │       │   │       ├── blend_zone/
         │       │   │       │   ├── factory.py
         │       │   │       │   ├── __init__.py
         │       │   │       │   ├── ivalidator.py
         │       │   │       │   └── validator.py
         │       │   │       ├── dwell/
         │       │   │       │   ├── factory.py
         │       │   │       │   ├── __init__.py
         │       │   │       │   ├── ivalidator.py
         │       │   │       │   └── validator.py
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       ├── provides.py
         │       │   │       └── rule.py
         │       │   ├── script/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── ilinter.py
         │       │   │   ├── __init__.py
         │       │   │   ├── linter.py
         │       │   │   └── provides.py
         │       │   └── validator/
         │       │       ├── dependencies.py
         │       │       ├── factory.py
         │       │       ├── __init__.py
         │       │       ├── ivalidator.py
         │       │       ├── provides.py
         │       │       └── validator.py
         │       ├── motor/
         │       │   ├── drive_mode_resolver.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── interface_resolver.py
         │       │   └── wire_mode_converter.py
         │       ├── parser/
         │       │   ├── commands/
         │       │   │   ├── config/
         │       │   │   │   ├── accel.py
         │       │   │   │   ├── elbow.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── motor.py
         │       │   │   │   ├── override.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── speed.py
         │       │   │   │   ├── syntax.py
         │       │   │   │   ├── tool_orient.py
         │       │   │   │   └── zone.py
         │       │   │   ├── flow/
         │       │   │   │   ├── disable.py
         │       │   │   │   ├── enable.py
         │       │   │   │   ├── estop.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── hold.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── resume.py
         │       │   │   │   ├── sync.py
         │       │   │   │   └── wait.py
         │       │   │   ├── frame/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── provides.py
         │       │   │   │   ├── reset.py
         │       │   │   │   └── set.py
         │       │   │   ├── icommand_parser.py
         │       │   │   ├── icommand_parser_provider.py
         │       │   │   ├── icommand_parser_provides.py
         │       │   │   ├── __init__.py
         │       │   │   ├── macro/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── jump.py
         │       │   │   │   ├── pallet_def.py
         │       │   │   │   ├── pallet_move.py
         │       │   │   │   └── provides.py
         │       │   │   ├── motion/
         │       │   │   │   ├── approach.py
         │       │   │   │   ├── arc.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── home.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── jog_axis.py
         │       │   │   │   ├── jog_joint.py
         │       │   │   │   ├── joint.py
         │       │   │   │   ├── linear.py
         │       │   │   │   ├── probe.py
         │       │   │   │   ├── provides.py
         │       │   │   │   └── retract.py
         │       │   │   ├── parameter/
         │       │   │   │   ├── extractor.py
         │       │   │   │   └── __init__.py
         │       │   │   └── tool/
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       ├── provides.py
         │       │   │       ├── pump.py
         │       │   │       ├── tool.py
         │       │   │       └── valve.py
         │       │   ├── dependencies.py
         │       │   ├── factory.py
         │       │   ├── __init__.py
         │       │   ├── instruction/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iparser.py
         │       │   │   ├── parser.py
         │       │   │   └── provides.py
         │       │   ├── iparser.py
         │       │   ├── lexer/
         │       │   │   ├── factory.py
         │       │   │   ├── ilexer.py
         │       │   │   ├── __init__.py
         │       │   │   ├── lexer.py
         │       │   │   └── provides.py
         │       │   ├── parser.py
         │       │   ├── provides.py
         │       │   └── splitter/
         │       │       ├── factory.py
         │       │       ├── __init__.py
         │       │       ├── isplitter.py
         │       │       ├── provides.py
         │       │       └── splitter.py
         │       ├── protocol/
         │       │   ├── ibinary_actuator_frame_builder.py
         │       │   ├── ibinary_actuator_payload_unpacker.py
         │       │   ├── ibinary_frame_codec.py
         │       │   ├── ibinary_frame_packer.py
         │       │   ├── ibinary_frame_parser.py
         │       │   ├── ibinary_motion_frame_builder.py
         │       │   ├── ibinary_motion_payload_unpacker.py
         │       │   ├── ibinary_response_builder.py
         │       │   ├── ibinary_response_payload_unpacker.py
         │       │   ├── ibinary_system_frame_builder.py
         │       │   ├── ibinary_system_payload_unpacker.py
         │       │   └── __init__.py
         │       ├── repl/
         │       │   ├── context/
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   └── __init__.py
         │       ├── trajectory/
         │       │   ├── avoidance/
         │       │   │   ├── bypass/
         │       │   │   │   ├── arc/
         │       │   │   │   │   ├── calculator.py
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── icalculator.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   └── provides.py
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── planner/
         │       │   │   │   │   ├── dependencies.py
         │       │   │   │   │   ├── factory.py
         │       │   │   │   │   ├── __init__.py
         │       │   │   │   │   ├── iplanner.py
         │       │   │   │   │   ├── planner.py
         │       │   │   │   │   └── provides.py
         │       │   │   │   └── provides.py
         │       │   │   ├── __init__.py
         │       │   │   ├── router/
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── irouter.py
         │       │   │   │   ├── provides.py
         │       │   │   │   └── router.py
         │       │   │   ├── shape/
         │       │   │   │   ├── dependencies.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── iplanner.py
         │       │   │   │   ├── planner.py
         │       │   │   │   └── provides.py
         │       │   │   └── validation/
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       ├── ivalidator.py
         │       │   │       ├── provides.py
         │       │   │       └── validator.py
         │       │   ├── discretization/
         │       │   │   ├── circle/
         │       │   │   │   ├── circle.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icircle.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── provides.py
         │       │   │   ├── factory.py
         │       │   │   ├── __init__.py
         │       │   │   ├── line/
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── iline.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   ├── line.py
         │       │   │   │   └── provides.py
         │       │   │   ├── provides.py
         │       │   │   └── rectangle/
         │       │   │       ├── factory.py
         │       │   │       ├── __init__.py
         │       │   │       ├── irectangle.py
         │       │   │       ├── provides.py
         │       │   │       └── rectangle.py
         │       │   ├── __init__.py
         │       │   ├── metrics/
         │       │   │   ├── bottleneck/
         │       │   │   │   ├── detector.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── idetector.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── provides.py
         │       │   │   ├── cycle/
         │       │   │   │   ├── calculator.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── icalculator.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── provides.py
         │       │   │   ├── factory.py
         │       │   │   ├── imetrics.py
         │       │   │   ├── __init__.py
         │       │   │   ├── metrics.py
         │       │   │   ├── profile/
         │       │   │   │   ├── analyzer.py
         │       │   │   │   ├── factory.py
         │       │   │   │   ├── ianalyzer.py
         │       │   │   │   ├── __init__.py
         │       │   │   │   └── provides.py
         │       │   │   ├── provides.py
         │       │   │   └── summary/
         │       │   │       ├── builder.py
         │       │   │       ├── dependencies.py
         │       │   │       ├── factory.py
         │       │   │       ├── ibuilder.py
         │       │   │       ├── __init__.py
         │       │   │       └── provides.py
         │       │   ├── plan/
         │       │   │   ├── factory.py
         │       │   │   ├── imutable.py
         │       │   │   ├── __init__.py
         │       │   │   ├── iplan.py
         │       │   │   ├── iread_only.py
         │       │   │   ├── plan.py
         │       │   │   └── provides.py
         │       │   └── validation/
         │       │       ├── dependencies.py
         │       │       ├── factory.py
         │       │       ├── feedrate/
         │       │       │   ├── factory.py
         │       │       │   ├── __init__.py
         │       │       │   ├── ivalidator.py
         │       │       │   ├── provides.py
         │       │       │   └── validator.py
         │       │       ├── __init__.py
         │       │       ├── plan/
         │       │       │   ├── dependencies.py
         │       │       │   ├── factory.py
         │       │       │   ├── __init__.py
         │       │       │   ├── ivalidator.py
         │       │       │   ├── provides.py
         │       │       │   └── validator.py
         │       │       ├── provides.py
         │       │       └── waypoint/
         │       │           ├── factory.py
         │       │           ├── __init__.py
         │       │           ├── ivalidator.py
         │       │           ├── provides.py
         │       │           └── validator.py
         │       └── transformation/
         │           ├── factory.py
         │           ├── __init__.py
         │           ├── itransformer.py
         │           ├── provides.py
         │           └── transformer.py
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
         │   │   ├── bundle.py
         │   │   ├── compile/
         │   │   │   ├── definition.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── error/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   ├── ihandler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   ├── inspection/
         │   │   │   │   ├── framing/
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── header/
         │   │   │   │   │   │   ├── factory.py
         │   │   │   │   │   │   ├── formatter.py
         │   │   │   │   │   │   ├── iformatter.py
         │   │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   │   └── provides.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── provides.py
         │   │   │   │   │   └── trailer/
         │   │   │   │   │       ├── factory.py
         │   │   │   │   │       ├── formatter.py
         │   │   │   │   │       ├── iformatter.py
         │   │   │   │   │       ├── __init__.py
         │   │   │   │   │       └── provides.py
         │   │   │   │   ├── hex/
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── formatter.py
         │   │   │   │   │   ├── iformatter.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   └── provides.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── payload/
         │   │   │   │   │   ├── dispatch/
         │   │   │   │   │   │   ├── dependencies.py
         │   │   │   │   │   │   ├── factory.py
         │   │   │   │   │   │   ├── formatter.py
         │   │   │   │   │   │   ├── iformatter.py
         │   │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   │   └── provides.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   ├── joint/
         │   │   │   │   │   │   ├── factory.py
         │   │   │   │   │   │   ├── formatter.py
         │   │   │   │   │   │   ├── iformatter.py
         │   │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   │   └── provides.py
         │   │   │   │   │   ├── provides.py
         │   │   │   │   │   └── tool/
         │   │   │   │   │       ├── factory.py
         │   │   │   │   │       ├── formatter.py
         │   │   │   │   │       ├── iformatter.py
         │   │   │   │   │       ├── __init__.py
         │   │   │   │   │       └── provides.py
         │   │   │   │   └── presentation/
         │   │   │   │       ├── factory.py
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── program/
         │   │   │   │       │   ├── factory.py
         │   │   │   │       │   ├── __init__.py
         │   │   │   │       │   ├── ipresenter.py
         │   │   │   │       │   ├── presenter.py
         │   │   │   │       │   └── provides.py
         │   │   │   │       ├── provides.py
         │   │   │   │       └── step/
         │   │   │   │           ├── dependencies.py
         │   │   │   │           ├── factory.py
         │   │   │   │           ├── __init__.py
         │   │   │   │           ├── ipresenter.py
         │   │   │   │           ├── presenter.py
         │   │   │   │           └── provides.py
         │   │   │   ├── provides.py
         │   │   │   └── telemetry/
         │   │   │       ├── factory.py
         │   │   │       ├── formatter.py
         │   │   │       ├── iformatter.py
         │   │   │       ├── __init__.py
         │   │   │       └── provides.py
         │   │   ├── decompile/
         │   │   │   ├── definition.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── error/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   ├── ihandler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── disassemble/
         │   │   │   ├── definition.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── error/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   ├── ihandler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── format/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── formatter.py
         │   │   │   │   ├── iformatter.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── export/
         │   │   │   ├── definition.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── error/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   ├── ihandler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── factory.py
         │   │   ├── idefinition.py
         │   │   ├── iexecutor.py
         │   │   ├── info/
         │   │   │   ├── definition.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── __init__.py
         │   │   ├── lint/
         │   │   │   ├── definition.py
         │   │   │   ├── dependencies.py
         │   │   │   ├── error/
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── handler.py
         │   │   │   │   ├── ihandler.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── executor.py
         │   │   │   ├── factory.py
         │   │   │   ├── __init__.py
         │   │   │   └── provides.py
         │   │   ├── provides.py
         │   │   └── repl/
         │   │       ├── definition.py
         │   │       ├── dependencies.py
         │   │       ├── executor.py
         │   │       ├── factory.py
         │   │       ├── __init__.py
         │   │       └── provides.py
         │   ├── compiler/
         │   │   ├── binary/
         │   │   │   ├── factory.py
         │   │   │   └── __init__.py
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── config/
         │   │   ├── scara_geometry_scheme.json
         │   │   ├── scaralang.cfg
         │   │   └── scaralang.logo
         │   ├── decompiler/
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── disassembler/
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── exporter/
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── info/
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── __init__.py
         │   ├── kinematics/
         │   │   ├── factory.py
         │   │   └── __init__.py
         │   ├── linter/
         │   │   ├── __init__.py
         │   │   ├── script/
         │   │   │   ├── factory.py
         │   │   │   └── __init__.py
         │   │   └── validator/
         │   │       ├── factory.py
         │   │       └── __init__.py
         │   ├── parser/
         │   │   ├── factory.py
         │   │   ├── __init__.py
         │   │   └── instruction/
         │   │       ├── factory.py
         │   │       └── __init__.py
         │   ├── protocol/
         │   │   ├── ascii/
         │   │   │   ├── classifier/
         │   │   │   │   ├── classifier.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── iclassifier.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── __init__.py
         │   │   │   └── templates/
         │   │   │       ├── factory.py
         │   │   │       ├── __init__.py
         │   │   │       ├── itemplates.py
         │   │   │       ├── provides.py
         │   │   │       └── templates.py
         │   │   ├── binary/
         │   │   │   ├── builder/
         │   │   │   │   ├── actuator.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── motion.py
         │   │   │   │   ├── packer.py
         │   │   │   │   ├── provides.py
         │   │   │   │   └── system.py
         │   │   │   ├── checksum/
         │   │   │   │   ├── crc16_ccitt.py
         │   │   │   │   └── __init__.py
         │   │   │   ├── codec/
         │   │   │   │   ├── codec.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   ├── __init__.py
         │   │   │   ├── parser/
         │   │   │   │   ├── assembler/
         │   │   │   │   │   ├── assembler.py
         │   │   │   │   │   ├── factory.py
         │   │   │   │   │   ├── iassembler.py
         │   │   │   │   │   ├── __init__.py
         │   │   │   │   │   └── provides.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   ├── parser.py
         │   │   │   │   ├── provides.py
         │   │   │   │   ├── state.py
         │   │   │   │   └── unpacker/
         │   │   │   │       ├── actuator.py
         │   │   │   │       ├── factory.py
         │   │   │   │       ├── __init__.py
         │   │   │   │       ├── motion.py
         │   │   │   │       ├── provides.py
         │   │   │   │       ├── response.py
         │   │   │   │       └── system.py
         │   │   │   ├── response/
         │   │   │   │   ├── builder.py
         │   │   │   │   ├── dependencies.py
         │   │   │   │   ├── factory.py
         │   │   │   │   ├── __init__.py
         │   │   │   │   └── provides.py
         │   │   │   └── struct_format.py
         │   │   └── __init__.py
         │   └── trajectory/
         │       ├── avoidance/
         │       │   ├── bypass/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   ├── __init__.py
         │       │   ├── router/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   ├── shape/
         │       │   │   ├── dependencies.py
         │       │   │   ├── factory.py
         │       │   │   └── __init__.py
         │       │   └── validation/
         │       │       ├── dependencies.py
         │       │       ├── factory.py
         │       │       └── __init__.py
         │       ├── discretization/
         │       │   ├── factory.py
         │       │   └── __init__.py
         │       ├── __init__.py
         │       ├── metrics/
         │       │   ├── factory.py
         │       │   └── __init__.py
         │       ├── plan/
         │       │   ├── factory.py
         │       │   └── __init__.py
         │       └── validation/
         │           ├── factory.py
         │           └── __init__.py
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

     210 directories, 931 files
```
</details>

#### 🏗 Architecture & SOLID Principles

```
           ┌────────────────────────────────────────────────────────────────────────┐
           │                         CLI / Inbound Adapters                         │
           │        (Compile, Decompile, Disassemble, Lint, Info, Export, REPL)     │
           └──────┬─────────────────────────────────────────────────────┬───────────┘
                  │                Depends on Role Protocols            │
                  ▼                                                     ▼
     ┌─────────────────────────┐┌─────────────────────────┐┌─────────────────────────┐
     │      IScaraLinter       ││     IScaraCompiler      ││    IScaraDecompiler     │
     │(Validation/Diagnostics) ││(Plan/Binary Generation) ││ (Forward Kinematics/FK) │
     └────────────┬────────────┘└────────────┬────────────┘└────────────┬────────────┘
                  │                          │                          │
                  ▼                          ▼                          ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                                Application Services                                │
│  ┌──────────────────┐   ┌────────────────────┐   ┌──────────────────────────────┐  │
│  │    ScaraLexer    │   │    ScaraParser     │   │        ScaraCompiler         │  │
│  │  (Token Stream)  │   │ (Command Parsers)  │   │       (Macro Expander)       │  │
│  └──────────────────┘   └────────────────────┘   └──────────────────────────────┘  │
│  ┌──────────────────┐   ┌────────────────────┐   ┌──────────────────────────────┐  │
│  │KinematicsService │   │SafeTrajectoryRouter│   │        BinaryCompiler        │  │
│  │ (Solver + Bounds)│   │  (Bypass & Avoid)  │   │       (Step Generator)       │  │
│  └──────────────────┘   └────────────────────┘   └──────────────────────────────┘  │
│  ┌──────────────────┐   ┌────────────────────┐   ┌──────────────────────────────┐  │
│  │ScaraDisassembler │   │   ScaraExporter    │   │       ScaraDecompiler        │  │
│  │ (Frame Decoder)  │   │ (Multi-target Exp) │   │     (FK Pose Recovery)       │  │
│  └──────────────────┘   └────────────────────┘   └──────────────────────────────┘  │
└─────────────────────────────────────────┬──────────────────────────────────────────┘
                                          │ Operates on Pure Models
                                          ▼
┌────────────────────────────────────────────────────────────────────────────────────┐
│                                Pure Domain Models                                  │
│      (ScaraProgram, BinaryProgram, Waypoint, CartesianPose, ScaraJoints,           │
│       BypassArcGeometry, CircleGeometry, ScaraBounds, InstructionParam, MessageId) │
└────────────────────────────────────────────────────────────────────────────────────┘
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

**scaralang** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the `.scara` extension and compiled into validated Cartesian trajectories via a clean AST pipeline, with full bidirectional decompilation back from binary bytecode:

```
         ┌─────────────────────────┐                      ┌─────────────────────────┐
         │      .scara Source      │                      │    Decompiled Source    │
         │ (High-level DSL Script) │                      │ (_decompiled.scara DSL) │
         └────────────┬────────────┘                      └────────────▲────────────┘
           ScaraLexer │                                                │ ScaraDecompiler
                      ▼                                                │ (Reconstructed
         ┌─────────────────────────┐                                   │  Cartesian Poses)
         │      Token Stream       │                                   │
         └────────────┬────────────┘                      ┌────────────┴────────────┐
          ScaraParser │                                   │    Forward Kinematics   │
                      ▼                                   │    (solve_fk: s -> X)   │
         ┌─────────────────────────┐                      └────────────▲────────────┘
         │       Abstract AST      │                                   │ BinaryParser /
         └────────────┬────────────┘                                   │ Frame Unpacker
       ScaraCompiler  │ (Macros + Kinematics)                          │
                      ▼                                                │
      ┌───────────────────────────────┐                                │
      │        TrajectoryPlan         │                                │
      │  (Waypoints & Discretization) │                                │
      └───────────────┬───────────────┘                                │
       BinaryCompiler │ (Step Discretization)                          │
                      ▼                                                │
         ┌─────────────────────────┐                                   │
         │      BinaryProgram      │───────────────────────────────────┘
         │ (Wire Frames & Bytecode)│          Bidirectional Round-Trip
         └─────────────────────────┘
```

##### Dead Zone Avoidance & Safe Trajectory Routing Pipeline

When generating continuous trajectories or executing Cartesian linear moves (`MOVE_L`), paths that intersect the inner annular physical dead zone ($R_{\min} \approx 77.6\text{ mm}$ for default SCARA geometry) are automatically detected and rerouted via tangent arc geometry:

```
                           ┌──────────────────────────┐
                           │   ISafeTrajectoryRouter  │
                           │  (Segment P1 -> P2 Move) │
                           └────────────┬─────────────┘
                                        │
                                        ▼
                           ┌──────────────────────────┐
                           │   IDeadZoneValidator     │
                           │ (Annular & Line Check)   │
                           └────────────┬─────────────┘
                                        │
                     Intersects R_min?  │
                        ┌───────────────┴───────────────┐
                    No  │                               │ Yes
                        ▼                               ▼
             ┌─────────────────────┐        ┌─────────────────────────────┐
             │ Direct Linear Move  │        │   IDeadZoneBypassPlanner    │
             │   (P1 -> P2 Path)   │        │   (Selects Safe Bypass)     │
             └─────────────────────┘        └──────────────┬──────────────┘
                                                           │
                                                           ▼
                                            ┌─────────────────────────────┐
                                            │    ITangentArcCalculator    │
                                            │ (Computes BypassArcGeometry)│
                                            └──────────────┬──────────────┘
                                                           │
                                                           ▼
                                            ┌─────────────────────────────┐
                                            │   IAvoidanceShapePlanner    │
                                            │  (Discretizes Safe Arc)     │
                                            └──────────────┬──────────────┘
                                                           │
                                                           ▼
                                            ┌─────────────────────────────┐
                                            │  Safe Composite Trajectory  │
                                            │  (P1 -> Tangent -> Arc ->   │
                                            │        Tangent -> P2)       │
                                            └─────────────────────────────┘
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

##### 📁 Verification Scripts & Examples (`examples/` & `run.sh`)

The repository includes a comprehensive test and validation suite in [`examples/`](examples/) covering all motion primitives, coordinate frames, macro operations, and pneumatic controls:

| Script | Domain Feature | Output Artifacts |
|---|---|---|
| `01_homing.scara` | Multi-axis homing sequence | `01_homing.bin`, `.dis`, `_decompiled.scara` |
| `02_linear_motion.scara` | Linear Cartesian path interpolation (`MOVE_L`) | `02_linear_motion.bin`, `.dis`, `_decompiled.scara` |
| `03_joint_rapid.scara` | Rapid joint point-to-point motion (`MOVE_J`) | `03_joint_rapid.bin`, `.dis`, `_decompiled.scara` |
| `04_circular_arc.scara` | Clockwise / counter-clockwise arcs (`ARC_CW` / `ARC_CCW`) | `04_circular_arc.bin`, `.dis`, `_decompiled.scara` |
| `05_jump_arch.scara` | Parabolic arch pick-and-place transfer (`JUMP`) | `05_jump_arch.bin`, `.dis`, `_decompiled.scara` |
| `06_pneumatics.scara` | End-effector vacuum pump & blow-off valve control | `06_pneumatics.bin`, `.dis`, `_decompiled.scara` |
| `07_approach_retract.scara` | Vertical tool descent and safe retract (`APPROACH` / `RETRACT`) | `07_approach_retract.bin`, `.dis`, `_decompiled.scara` |
| `08_work_frames.scara` | Workpiece coordinate frame offsets (`FRAME USER` / `FRAME BASE`) | `08_work_frames.bin`, `.dis`, `_decompiled.scara` |
| `09_pallet_matrix.scara` | Grid pallet matrix indexing (`PALLET_DEF` / `MOVE_PALLET`) | `09_pallet_matrix.bin`, `.dis`, `_decompiled.scara` |
| `10_tangent_orientation.scara` | Automatic 4th-axis tool yaw tangent orientation | `10_tangent_orientation.bin`, `.dis`, `_decompiled.scara` |
| `11_zone_blending.scara` | Corner tolerance continuous path smoothing (`ZONE`) | `11_zone_blending.bin`, `.dis`, `_decompiled.scara` |
| `12_industrial_pick_place.scara` | Complete industrial assembly & palletizing cycle | `12_industrial_pick_place.bin`, `.dis`, `_decompiled.scara` |

To validate compilation, decompiler round-trip, and disassembly across all examples in a single pass:

```bash
# Execute automated batch compiler / decompiler verification
bash run.sh
```

#### 📡 SCARA Binary Wire Protocol & Codec

All binary wire communication between **scaralang**, **scarajectory**, **scaraemu**, and physical robot firmware is governed by deterministic packet framing:

##### Frame Header & Wire Format

Each binary wire frame consists of a 5-byte header, variable payload (0 to 64 bytes), and a 3-byte trailer (CRC-16-CCITT and EOF delimiter `0x0D`):

```
┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────────┬──────────────┬──────────────┐
│  SOF1 (0xAA) │  SOF2 (0x55) │  Msg ID (1B) │   SEQ (1B)   │  Length (1B) │   Payload (NB)   │  CRC16 (2B)  │  EOF (0x0D)  │
└──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────────┴──────────────┴──────────────┘
│<─────────────── 5-Byte Wire Header ──────────────────────>│  0..64 Bytes │<───── 3-Byte Wire Trailer ─────>│
```

##### Message Types & Payload Structure

| Message ID | Enum Identifier | Payload Structure | Description |
|---|:---:|---|---|
| `0x01` | `CMD_MOVE_JOINT_STEPS` | `j1..j4 (16B), duration_us (4B), feed (2B)` (22B) | Coordinated stepper motor joint step block with duration and feedrate. |
| `0x03` | `CMD_ENABLE` | Empty (`0 bytes`) | Energize stepper motor driver stages (holding torque). |
| `0x04` | `CMD_DISABLE` | Empty (`0 bytes`) | De-energize motor driver stages (free movement). |
| `0x05` | `CMD_ESTOP` | Empty (`0 bytes`) | Immediate hardware emergency stop and motion abort. |
| `0x06` | `CMD_HOME` | Empty (`0 bytes`) | Execute multi-axis homing sequence (Z -> J2 -> J1). |
| `0x07` | `CMD_HOLD` | Empty (`0 bytes`) | Trajectory feed hold / pause motion execution. |
| `0x08` | `CMD_RESUME` | Empty (`0 bytes`) | Resume suspended motion execution. |
| `0x09` | `CMD_JOG_JOINT` | `joint_id (1B), dir (1B), steps (2B)` (4B) | Incremental single joint rotational/linear jog. |
| `0x0A` | `CMD_SETPOS_STEPS` | `s1, s2, s3, s4 (16B)` | Force absolute step register position without motion. |
| `0x0B` | `CMD_TOOL_PUMP` | `tool_id (1B), state (1B)` (2B) | Vacuum suction pump actuation (`ON`/`OFF`). |
| `0x0C` | `CMD_TOOL_VALVE` | `tool_id (1B), state (1B)` (2B) | Pneumatic blow-off release valve actuation (`ON`/`OFF`). |
| `0x0D` | `CMD_WAIT` | `delay_ms (4B)` | Dwell delay execution for specified milliseconds. |
| `0x0E` | `CMD_OVERRIDE` | `percent (1B: 10..200)` | Dynamically scale path execution velocity in real time. |
| `0x0F` | `CMD_CONFIG_MOTOR` | `motor_mode (1B), axis_mask (1B)` (2B) | Select open-loop TMC2209 or closed-loop MKS SERVO42D. |
| `0x20` | `CMD_GET_STATUS` | Empty (`0 bytes`) | Query consolidated robot status and motion flags. |
| `0x21` | `CMD_GET_STEPS` | Empty (`0 bytes`) | Query current absolute joint step counters. |
| `0x22` | `CMD_GET_DIAGNOSTICS` | Empty (`0 bytes`) | Query extended controller diagnostics and memory stats. |
| `0x23` | `CMD_CLEAR_FAULT` | Empty (`0 bytes`) | Reset latched hardware fault condition. |
| `0x24` | `CMD_PING` | `timestamp_ms (4B)` | Real-time link health and latency measurement ping. |
| `0x30` | `CMD_BOOTLOADER` | Empty (`0 bytes`) | Reboot controller into USB BOOTSEL firmware update mode. |
| `0x80` | `RESP_ACK` | `acked_id (1B), q_count (1B)` (2B) | Positive command acknowledgment from robot controller. |
| `0x81` | `RESP_NACK` | `rejected_id (1B), error_code (1B)` (2B) | Negative command rejection with hardware error code. |
| `0x82` | `RESP_STATUS` | `state, substate, flags (3B), s1..s4 (16B)` (19B) | Real-time consolidated robot status and coordinates. |
| `0x83` | `RESP_STEPS` | `s1, s2, s3, s4 (16B)` | Current absolute joint step positions for all 4 axes. |
| `0x84` | `RESP_PONG` | `echo_timestamp_ms (4B)` | Heartbeat keepalive reply with round-trip timestamp. |
| `0x85` | `RESP_MOVE_EVENT` | `event_type (1B), step_index (4B)` (5B) | Trajectory waypoint start/complete execution notification. |
| `0x86` | `RESP_HOMING_EVENT` | `axis_mask (1B), status (1B)` (2B) | Multi-axis limit switch trigger event notification. |
| `0x88` | `RESP_DIAGNOSTICS` | Extended 56-byte payload | System diagnostics (CPU, free RAM, temperature, drops). |
| `0x89` | `RESP_FAULT_EVENT` | `fault_code (2B), axis (1B), info (1B)` (4B) | Critical hardware fault alert. |

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
from scaralang.infrastructure.compiler.factory import DefaultCompilerFactory

compiler = DefaultCompilerFactory.create()

try:
    plan = compiler.compile_to_binary(source="MOVE_J X 999.0 Y 999.0 Z 20.0")
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
| `scaralang/core/model/dsl/binary/program.py` | 21 | 0 | 100%|
| `scaralang/core/model/dsl/binary/step.py` | 20 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/arc_geometry.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_blend_state.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_context.py` | 26 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_pose_state.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/compiler_speed_state.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/compiler/control_waypoint_descriptor.py` | 16 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic.py` | 18 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic_code.py` | 23 | 0 | 100%|
| `scaralang/core/model/dsl/diagnostic/scara_diagnostic_severity.py` | 15 | 0 | 100%|
| `scaralang/core/model/dsl/exporter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/exporter/export_format.py` | 17 | 0 | 100%|
| `scaralang/core/model/dsl/linter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/dsl/linter/lint_context.py` | 22 | 0 | 100%|
| `scaralang/core/model/dsl/linter/lint_tool_state.py` | 14 | 0 | 100%|
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
| `scaralang/core/model/kinematics/axis_name.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/cartesian_pose.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/elbow_config.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/ik_status.py` | 18 | 0 | 100%|
| `scaralang/core/model/kinematics/joint_angle_bounds.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/joint_angles.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/joint_step_coordinates.py` | 16 | 0 | 100%|
| `scaralang/core/model/kinematics/link_dimensions.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/point_2d.py` | 14 | 0 | 100%|
| `scaralang/core/model/kinematics/point_3d.py` | 15 | 0 | 100%|
| `scaralang/core/model/kinematics/scara_bounds.py` | 22 | 0 | 100%|
| `scaralang/core/model/kinematics/scara_joints.py` | 19 | 0 | 100%|
| `scaralang/core/model/kinematics/scara_joints_2d.py` | 17 | 0 | 100%|
| `scaralang/core/model/kinematics/scara_joints_3d.py` | 18 | 0 | 100%|
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
| `scaralang/core/model/protocol/binary_payload_size.py` | 24 | 0 | 100%|
| `scaralang/core/model/protocol/error_code.py` | 21 | 0 | 100%|
| `scaralang/core/model/protocol/joint_steps.py` | 18 | 0 | 100%|
| `scaralang/core/model/protocol/manipulator_status.py` | 19 | 0 | 100%|
| `scaralang/core/model/protocol/message_id.py` | 41 | 0 | 100%|
| `scaralang/core/model/protocol/motor_wire_mode.py` | 14 | 0 | 100%|
| `scaralang/core/model/protocol/move_event_type.py` | 15 | 0 | 100%|
| `scaralang/core/model/protocol/tool_id.py` | 13 | 0 | 100%|
| `scaralang/core/model/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/repl/repl_dispatch_result.py` | 15 | 0 | 100%|
| `scaralang/core/model/repl/repl_pose_state.py` | 16 | 0 | 100%|
| `scaralang/core/model/repl/repl_session_context.py` | 21 | 0 | 100%|
| `scaralang/core/model/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/model/trajectory/arc_point.py` | 15 | 0 | 100%|
| `scaralang/core/model/trajectory/axis_peak_metric.py` | 17 | 0 | 100%|
| `scaralang/core/model/trajectory/bottleneck_incident.py` | 18 | 0 | 100%|
| `scaralang/core/model/trajectory/bypass_arc_geometry.py` | 10 | 0 | 100%|
| `scaralang/core/model/trajectory/circle_geometry.py` | 18 | 0 | 100%|
| `scaralang/core/model/trajectory/constraint_type.py` | 14 | 0 | 100%|
| `scaralang/core/model/trajectory/trajectory_cycle_report.py` | 18 | 0 | 100%|
| `scaralang/core/model/trajectory/validation_result.py` | 15 | 0 | 100%|
| `scaralang/core/model/trajectory/waypoint.py` | 19 | 0 | 100%|
| `scaralang/core/service/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/actuator/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/actuator/builder.py` | 28 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/actuator/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/actuator/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/actuator/ibuilder.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/compiler.py` | 64 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/compiler_dependencies.py` | 22 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/factory.py` | 32 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/icompiler.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/iparser.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tokens/parser.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/builder.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/command/tool/ibuilder.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/compiler.py` | 31 | 0 | 100%|
| `scaralang/core/service/compiler/binary/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/binary/icompiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/calculator.py` | 39 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/metrics/icalculator.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/compiler.py` | 36 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/icompiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/binary/motion/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/binary/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/discretizer/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/discretizer/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/discretizer/discretizer.py` | 46 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/discretizer/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/discretizer/idiscretizer.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/dispatcher/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/dispatcher/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/dispatcher/dispatcher.py` | 36 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/dispatcher/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/dispatcher/idispatcher.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/duration/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/duration/calculator.py` | 29 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/duration/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/binary/step/duration/icalculator.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/compiler.py` | 28 | 0 | 100%|
| `scaralang/core/service/compiler/context/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/context/factory.py` | 37 | 0 | 100%|
| `scaralang/core/service/compiler/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/icompiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/dependencies.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/factory.py` | 26 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/pipeline/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/pipeline/dependencies.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/pipeline/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/pipeline/ipipeline.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/pipeline/pipeline.py` | 38 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/processor/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/processor/dependencies.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/processor/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/processor/iprocessor.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/processor/processor.py` | 27 | 0 | 100%|
| `scaralang/core/service/compiler/instruction/provides.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/macro/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/macro/factory.py` | 29 | 0 | 100%|
| `scaralang/core/service/compiler/macro/frame/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/frame/expander.py` | 30 | 0 | 100%|
| `scaralang/core/service/compiler/macro/frame/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/macro/iexpander.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/macro/jump/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/jump/expander.py` | 34 | 0 | 100%|
| `scaralang/core/service/compiler/macro/jump/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet/expander.py` | 47 | 0 | 100%|
| `scaralang/core/service/compiler/macro/pallet/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/macro/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/macro/tangent/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/macro/tangent/expander.py` | 24 | 0 | 100%|
| `scaralang/core/service/compiler/macro/tangent/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/plan/ast/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/plan/ast/compiler.py` | 33 | 0 | 100%|
| `scaralang/core/service/compiler/plan/ast/factory.py` | 31 | 0 | 100%|
| `scaralang/core/service/compiler/plan/ast/icompiler.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/plan/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/plan/factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/plan/provides.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/plan/script/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/plan/script/compiler.py` | 44 | 0 | 100%|
| `scaralang/core/service/compiler/plan/script/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/plan/script/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/plan/script/icompiler.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/compiler.py` | 49 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/waypoint/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/waypoint/builder.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/waypoint/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/control/waypoint/ibuilder.py` | 17 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/factory.py` | 27 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/icompiler.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/calculator/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/calculator/calculator.py` | 40 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/calculator/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/calculator/icalculator.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/compiler.py` | 43 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/interpolation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/interpolation/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/interpolation/iinterpolator.py` | 16 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/interpolation/interpolator.py` | 52 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/waypoint/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/waypoint/builder.py` | 23 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/waypoint/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/arc/waypoint/ibuilder.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/compiler.py` | 49 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/itangent_heading_calculator.py` | 15 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/tangent_heading_calculator.py` | 22 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/cartesian/tangent_heading_calculator_factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/compiler.py` | 29 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/isub_compiler.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/vertical/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/vertical/compiler.py` | 37 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/motion/vertical/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/compiler.py` | 53 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/state/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/compiler.py` | 36 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/waypoint/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/waypoint/builder.py` | 21 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/waypoint/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/primitive/tool/waypoint/ibuilder.py` | 18 | 0 | 100%|
| `scaralang/core/service/compiler/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/decompiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/decompiler/decompiler.py` | 37 | 0 | 100%|
| `scaralang/core/service/decompiler/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/decompiler/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/dependencies.py` | 20 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/frame.py` | 72 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/iframe.py` | 15 | 0 | 100%|
| `scaralang/core/service/decompiler/frame/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/decompiler/idecompiler.py` | 17 | 0 | 100%|
| `scaralang/core/service/decompiler/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/disassembler/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/disassembler/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/disassembler/disassembler.py` | 39 | 0 | 100%|
| `scaralang/core/service/disassembler/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/actuator_decoder.py` | 38 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/factory.py` | 22 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/idecoder.py` | 16 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/joint_steps_decoder.py` | 26 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/decoder/system_decoder.py` | 34 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/factory.py` | 22 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/frame.py` | 30 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/iframe.py` | 16 | 0 | 100%|
| `scaralang/core/service/disassembler/frame/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/disassembler/idisassembler.py` | 19 | 0 | 100%|
| `scaralang/core/service/disassembler/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/exporter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/csv/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/csv/exporter.py` | 21 | 0 | 100%|
| `scaralang/core/service/exporter/csv/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/csv/iexporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/dependencies.py` | 22 | 0 | 100%|
| `scaralang/core/service/exporter/exporter.py` | 49 | 0 | 100%|
| `scaralang/core/service/exporter/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/exporter.py` | 24 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/gcode/iexporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/iexporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/json/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/json/exporter.py` | 20 | 0 | 100%|
| `scaralang/core/service/exporter/json/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/json/iexporter.py` | 17 | 0 | 100%|
| `scaralang/core/service/exporter/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/exporter/scara/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/scara/exporter.py` | 52 | 0 | 100%|
| `scaralang/core/service/exporter/scara/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/scara/formatter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/scara/formatter/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/scara/formatter/formatter.py` | 47 | 0 | 100%|
| `scaralang/core/service/exporter/scara/formatter/iformatter.py` | 16 | 0 | 100%|
| `scaralang/core/service/exporter/scara/iexporter.py` | 19 | 0 | 100%|
| `scaralang/core/service/exporter/scara/serializer.py` | 21 | 0 | 100%|
| `scaralang/core/service/exporter/scara/source_generator.py` | 25 | 0 | 100%|
| `scaralang/core/service/exporter/svg/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/exporter/svg/exporter.py` | 28 | 0 | 100%|
| `scaralang/core/service/exporter/svg/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/exporter/svg/iexporter.py` | 18 | 0 | 100%|
| `scaralang/core/service/info/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/info/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/info/iinfo.py` | 16 | 0 | 100%|
| `scaralang/core/service/info/info.py` | 44 | 0 | 100%|
| `scaralang/core/service/info/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/kinematics/envelope/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/envelope/envelope.py` | 38 | 0 | 100%|
| `scaralang/core/service/kinematics/envelope/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/kinematics/envelope/ienvelope.py` | 24 | 0 | 100%|
| `scaralang/core/service/kinematics/factory.py` | 30 | 0 | 100%|
| `scaralang/core/service/kinematics/profile/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/profile/default_scara_profile.py` | 34 | 0 | 100%|
| `scaralang/core/service/kinematics/profile/factory.py` | 36 | 0 | 100%|
| `scaralang/core/service/kinematics/provides.py` | 20 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/planar/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/planar/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/planar/isolver.py` | 18 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/planar/solver.py` | 57 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/spatial/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/spatial/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/spatial/isolver.py` | 21 | 0 | 100%|
| `scaralang/core/service/kinematics/solver/spatial/solver.py` | 48 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/converter.py` | 36 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/kinematics/transmission/iconverter.py` | 18 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/boundary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/boundary/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/boundary/iservice.py` | 17 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/boundary/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/boundary/service.py` | 41 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/evaluator.py` | 67 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/kinematics/workspace/ievaluator.py` | 19 | 0 | 100%|
| `scaralang/core/service/linter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/context/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/context/factory.py` | 22 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/formatter.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/iformatter.py` | 15 | 0 | 100%|
| `scaralang/core/service/linter/diagnostic/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/linter/factory.py` | 24 | 0 | 100%|
| `scaralang/core/service/linter/ilinter.py` | 19 | 0 | 100%|
| `scaralang/core/service/linter/linter.py` | 37 | 0 | 100%|
| `scaralang/core/service/linter/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/linter/rules/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/irule.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/calibration/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/calibration/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/calibration/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/calibration/validator.py` | 22 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/duplicate/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/duplicate/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/duplicate/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/duplicate/validator.py` | 39 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/provides.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/motion/rule.py` | 33 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/conflict/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/conflict/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/conflict/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/conflict/validator.py` | 32 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/flyby/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/flyby/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/flyby/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/flyby/validator.py` | 26 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/provides.py` | 20 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/redundancy/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/redundancy/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/redundancy/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/redundancy/validator.py` | 32 | 0 | 100%|
| `scaralang/core/service/linter/rules/pneumatic/rule.py` | 45 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/homing/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/homing/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/homing/ivalidator.py` | 17 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/homing/validator.py` | 20 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/mode/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/mode/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/mode/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/mode/validator.py` | 35 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/provides.py` | 20 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/rule.py` | 38 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/zone/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/zone/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/zone/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/state/zone/validator.py` | 38 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/blend_zone/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/blend_zone/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/blend_zone/ivalidator.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/blend_zone/validator.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/dwell/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/dwell/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/dwell/ivalidator.py` | 17 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/dwell/validator.py` | 27 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/provides.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/rules/timing/rule.py` | 33 | 0 | 100%|
| `scaralang/core/service/linter/script/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/script/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/linter/script/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/linter/script/ilinter.py` | 15 | 0 | 100%|
| `scaralang/core/service/linter/script/linter.py` | 37 | 0 | 100%|
| `scaralang/core/service/linter/script/provides.py` | 16 | 0 | 100%|
| `scaralang/core/service/linter/validator/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/linter/validator/dependencies.py` | 20 | 0 | 100%|
| `scaralang/core/service/linter/validator/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/linter/validator/ivalidator.py` | 14 | 0 | 100%|
| `scaralang/core/service/linter/validator/provides.py` | 16 | 0 | 100%|
| `scaralang/core/service/linter/validator/validator.py` | 43 | 0 | 100%|
| `scaralang/core/service/motor/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/motor/drive_mode_resolver.py` | 31 | 0 | 100%|
| `scaralang/core/service/motor/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/motor/interface_resolver.py` | 31 | 0 | 100%|
| `scaralang/core/service/motor/wire_mode_converter.py` | 25 | 0 | 100%|
| `scaralang/core/service/parser/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/accel.py` | 33 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/elbow.py` | 40 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/factory.py` | 31 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/motor.py` | 44 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/override.py` | 33 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/provides.py` | 21 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/speed.py` | 39 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/syntax.py` | 52 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/tool_orient.py` | 41 | 0 | 100%|
| `scaralang/core/service/parser/commands/config/zone.py` | 41 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/disable.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/enable.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/estop.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/factory.py` | 31 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/hold.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/provides.py` | 21 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/resume.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/sync.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/flow/wait.py` | 37 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/factory.py` | 21 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/provides.py` | 16 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/reset.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/frame/set.py` | 27 | 0 | 100%|
| `scaralang/core/service/parser/commands/icommand_parser.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/commands/icommand_parser_provider.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/commands/icommand_parser_provides.py` | 15 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/jump.py` | 30 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/pallet_def.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/pallet_move.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/commands/macro/provides.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/approach.py` | 26 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/arc.py` | 29 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/factory.py` | 35 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/home.py` | 24 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/jog_axis.py` | 41 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/jog_joint.py` | 37 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/joint.py` | 26 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/linear.py` | 26 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/probe.py` | 26 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/provides.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/motion/retract.py` | 26 | 0 | 100%|
| `scaralang/core/service/parser/commands/parameter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/parameter/extractor.py` | 50 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/factory.py` | 23 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/provides.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/pump.py` | 35 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/tool.py` | 36 | 0 | 100%|
| `scaralang/core/service/parser/commands/tool/valve.py` | 35 | 0 | 100%|
| `scaralang/core/service/parser/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/parser/instruction/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/instruction/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/parser/instruction/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/parser/instruction/iparser.py` | 20 | 0 | 100%|
| `scaralang/core/service/parser/instruction/parser.py` | 59 | 0 | 100%|
| `scaralang/core/service/parser/instruction/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/parser/iparser.py` | 19 | 0 | 100%|
| `scaralang/core/service/parser/lexer/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/lexer/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/lexer/ilexer.py` | 16 | 0 | 100%|
| `scaralang/core/service/parser/lexer/lexer.py` | 45 | 0 | 100%|
| `scaralang/core/service/parser/lexer/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/parser/parser.py` | 34 | 0 | 100%|
| `scaralang/core/service/parser/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/parser/splitter/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/parser/splitter/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/parser/splitter/isplitter.py` | 17 | 0 | 100%|
| `scaralang/core/service/parser/splitter/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/parser/splitter/splitter.py` | 28 | 0 | 100%|
| `scaralang/core/service/protocol/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_actuator_frame_builder.py` | 17 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_actuator_payload_unpacker.py` | 15 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_frame_codec.py` | 17 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_frame_packer.py` | 17 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_frame_parser.py` | 18 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_motion_frame_builder.py` | 16 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_motion_payload_unpacker.py` | 15 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_response_builder.py` | 21 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_response_payload_unpacker.py` | 15 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_system_frame_builder.py` | 19 | 0 | 100%|
| `scaralang/core/service/protocol/ibinary_system_payload_unpacker.py` | 15 | 0 | 100%|
| `scaralang/core/service/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/repl/context/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/repl/context/factory.py` | 25 | 0 | 100%|
| `scaralang/core/service/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/arc/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/arc/calculator.py` | 21 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/arc/factory.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/arc/icalculator.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/arc/provides.py` | 13 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/dependencies.py` | 12 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/factory.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/factory.py` | 15 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/iplanner.py` | 12 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/planner.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/planner/provides.py` | 12 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/bypass/provides.py` | 10 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/irouter.py` | 15 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/router/router.py` | 35 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/dependencies.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/factory.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/iplanner.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/planner.py` | 48 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/shape/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/validation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/validation/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/validation/ivalidator.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/validation/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/avoidance/validation/validator.py` | 39 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/circle/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/circle/circle.py` | 43 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/circle/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/circle/icircle.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/circle/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/factory.py` | 26 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/line/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/line/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/line/iline.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/line/line.py` | 22 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/line/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/provides.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/rectangle/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/rectangle/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/rectangle/irectangle.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/rectangle/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/discretization/rectangle/rectangle.py` | 22 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/detector.py` | 41 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/idetector.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/bottleneck/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/calculator.py` | 47 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/icalculator.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/cycle/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/imetrics.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/metrics.py` | 44 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/analyzer.py` | 60 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/ianalyzer.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/profile/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/builder.py` | 36 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/dependencies.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/ibuilder.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/metrics/summary/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/imutable.py` | 21 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/iplan.py` | 13 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/iread_only.py` | 20 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/plan.py` | 42 | 0 | 100%|
| `scaralang/core/service/trajectory/plan/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/factory.py` | 28 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/ivalidator.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/feedrate/validator.py` | 28 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/dependencies.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/ivalidator.py` | 16 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/plan/validator.py` | 47 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/provides.py` | 18 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/factory.py` | 19 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/ivalidator.py` | 17 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/trajectory/validation/waypoint/validator.py` | 38 | 0 | 100%|
| `scaralang/core/service/transformation/__init__.py` | 9 | 0 | 100%|
| `scaralang/core/service/transformation/factory.py` | 18 | 0 | 100%|
| `scaralang/core/service/transformation/itransformer.py` | 17 | 0 | 100%|
| `scaralang/core/service/transformation/provides.py` | 14 | 0 | 100%|
| `scaralang/core/service/transformation/transformer.py` | 40 | 0 | 100%|
| `scaralang/engine.py` | 60 | 0 | 100%|
| `scaralang/infrastructure/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/engine.py` | 43 | 0 | 100%|
| `scaralang/infrastructure/cli/icli.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/irepl_single_command_compiler.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/repl_single_command_compiler.py` | 51 | 0 | 100%|
| `scaralang/infrastructure/cli/repl/compiler/repl_single_command_compiler_factory.py` | 32 | 0 | 100%|
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
| `scaralang/infrastructure/cli/setup/factory.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/keys.py` | 23 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/opt_validator.py` | 35 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/options.py` | 13 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/registry.py` | 29 | 0 | 100%|
| `scaralang/infrastructure/cli/setup/validator.py` | 38 | 0 | 100%|
| `scaralang/infrastructure/command/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/bundle.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/compile/dependencies.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/ihandler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/error/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/executor.py` | 60 | 0 | 100%|
| `scaralang/infrastructure/command/compile/factory.py` | 33 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/factory.py` | 23 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/header/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/header/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/header/formatter.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/header/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/header/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/trailer/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/trailer/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/trailer/formatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/trailer/iformatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/framing/trailer/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/hex/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/hex/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/hex/formatter.py` | 21 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/hex/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/hex/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/dependencies.py` | 22 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/factory.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/formatter.py` | 49 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/dispatch/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/factory.py` | 33 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint/factory.py` | 21 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint/formatter.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/joint/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/provides.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool/factory.py` | 21 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool/formatter.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool/iformatter.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/payload/tool/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/factory.py` | 34 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program/factory.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program/ipresenter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program/presenter.py` | 27 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/program/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/dependencies.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/factory.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/ipresenter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/presenter.py` | 37 | 0 | 100%|
| `scaralang/infrastructure/command/compile/inspection/presentation/step/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/compile/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/formatter.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/compile/telemetry/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/dependencies.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/ihandler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/error/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/executor.py` | 45 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/factory.py` | 27 | 0 | 100%|
| `scaralang/infrastructure/command/decompile/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/dependencies.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/ihandler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/error/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/executor.py` | 61 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/factory.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/formatter.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/iformatter.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/format/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/disassemble/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/export/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/export/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/export/dependencies.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/ihandler.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/command/export/error/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/export/executor.py` | 53 | 0 | 100%|
| `scaralang/infrastructure/command/export/factory.py` | 36 | 0 | 100%|
| `scaralang/infrastructure/command/export/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/factory.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/idefinition.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/iexecutor.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/info/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/info/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/info/executor.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/command/info/factory.py` | 22 | 0 | 100%|
| `scaralang/infrastructure/command/info/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/lint/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/lint/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/lint/dependencies.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/handler.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/ihandler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/lint/error/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/lint/executor.py` | 47 | 0 | 100%|
| `scaralang/infrastructure/command/lint/factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/command/lint/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/command/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/command/repl/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/command/repl/definition.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/repl/dependencies.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/command/repl/executor.py` | 84 | 0 | 100%|
| `scaralang/infrastructure/command/repl/factory.py` | 29 | 0 | 100%|
| `scaralang/infrastructure/command/repl/provides.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/compiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/compiler/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/compiler/binary/factory.py` | 43 | 0 | 100%|
| `scaralang/infrastructure/compiler/factory.py` | 31 | 0 | 100%|
| `scaralang/infrastructure/decompiler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/decompiler/factory.py` | 33 | 0 | 100%|
| `scaralang/infrastructure/disassembler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/disassembler/factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/exporter/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/exporter/factory.py` | 27 | 0 | 100%|
| `scaralang/infrastructure/info/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/info/factory.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/kinematics/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/kinematics/factory.py` | 22 | 0 | 100%|
| `scaralang/infrastructure/linter/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/linter/script/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/linter/script/factory.py` | 23 | 0 | 100%|
| `scaralang/infrastructure/linter/validator/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/linter/validator/factory.py` | 27 | 0 | 100%|
| `scaralang/infrastructure/parser/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/parser/factory.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/parser/instruction/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/parser/instruction/factory.py` | 30 | 0 | 100%|
| `scaralang/infrastructure/protocol/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/classifier/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/classifier/classifier.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/classifier/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/classifier/iclassifier.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/classifier/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/templates/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/templates/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/templates/itemplates.py` | 15 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/templates/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/ascii/templates/templates.py` | 49 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/actuator.py` | 33 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/factory.py` | 22 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/motion.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/packer.py` | 35 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/provides.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/builder/system.py` | 40 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/checksum/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/checksum/crc16_ccitt.py` | 35 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/codec/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/codec/codec.py` | 32 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/codec/dependencies.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/codec/factory.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/codec/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/assembler/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/assembler/assembler.py` | 32 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/assembler/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/assembler/iassembler.py` | 16 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/assembler/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/factory.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/parser.py` | 90 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/provides.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/state.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/actuator.py` | 33 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/factory.py` | 21 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/motion.py` | 24 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/provides.py` | 20 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/response.py` | 29 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/parser/unpacker/system.py` | 34 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/response/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/response/builder.py` | 36 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/response/dependencies.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/response/factory.py` | 19 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/response/provides.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/protocol/binary/struct_format.py` | 26 | 0 | 100%|
| `scaralang/infrastructure/trajectory/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/bypass/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/bypass/dependencies.py` | 12 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/bypass/factory.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/router/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/router/dependencies.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/router/factory.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/shape/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/shape/dependencies.py` | 17 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/shape/factory.py` | 25 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/validation/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/validation/dependencies.py` | 14 | 0 | 100%|
| `scaralang/infrastructure/trajectory/avoidance/validation/factory.py` | 28 | 0 | 100%|
| `scaralang/infrastructure/trajectory/discretization/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/discretization/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/trajectory/metrics/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/metrics/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/trajectory/plan/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/plan/factory.py` | 18 | 0 | 100%|
| `scaralang/infrastructure/trajectory/validation/__init__.py` | 9 | 0 | 100%|
| `scaralang/infrastructure/trajectory/validation/factory.py` | 21 | 0 | 100%|
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
| **Total** | 18225 | 0 | 100% |

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
from scaralang.infrastructure.compiler.factory import DefaultCompilerFactory
from scaralang.infrastructure.decompiler.factory import DefaultDecompilerFactory
from scaralang.infrastructure.linter.validator.factory import DefaultScriptValidatorFactory

# Initialize fine-grained role services via their default infrastructure factories
validator = DefaultScriptValidatorFactory.create().validator
compiler = DefaultCompilerFactory.create()
decompiler = DefaultDecompilerFactory.create()

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
    # 2. Compile directly to binary program package and raw bytecode
    binary_prog = compiler.compile_to_binary(source=script)
    raw_bytes = compiler.compile_to_bytes(source=script)
    telemetry = compiler.get_program_telemetry(program=binary_prog)
    print(f"Generated {len(raw_bytes)} bytes of binary bytecode.")
    print(f"Total motor steps: {len(binary_prog.steps)}")
    print(f"Trajectory execution time: {telemetry.duration_s:.2f} s")

    # 3. Decompile binary bytecode back into high-level SCARA DSL script
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
