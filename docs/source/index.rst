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

🏗 Architecture & SOLID Principles
--------------------------------------------------------------------------------

.. code-block:: text

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

SOLID Principles Compliance
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **S — Single Responsibility Principle (SRP)**:
  Every module, class, and service has exactly one clearly bounded reason to change. Parser and compiler logic is decomposed into dedicated handlers (``MotionCommandParser``, ``ConfigCommandParser``, ``PalletMacroExpander``, ``StepDiscretizer``) rather than a monolithic interpreter. Strict limit of <= 15 methods per class across the entire codebase enforced by automated Quality Gate.
* **O — Open/Closed Principle (OCP)**:
  The DSL parser, macro expanders, and exporters are open for extension without modifying existing code. Extensible Chain of Responsibility and dispatcher pattern allow registering new instruction handlers and export targets seamlessly.
* **L — Liskov Substitution Principle (LSP)**:
  Pure structural subtyping via Python ``@runtime_checkable Protocol`` definitions. Concrete classes never inherit from abstract protocols, ensuring complete structural interchangeability.
* **I — Interface Segregation Principle (ISP)**:
  Unified role protocols (``IScaraCompiler``, ``IScaraDecompiler``, ``IScaraDisassembler``, ``IScaraLinter``, ``IScaraParser``, ``IScaraLexer``, ``IScaraExporter``, ``IScaraInfoProvider``). Clients depend strictly on the minimal methods they call.
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
* **Bidirectional Decompiler**: Full binary-to-source decompilation reconstructing high-level SCARA DSL scripts from compiled bytecode frames (``scarac decompile``).
* **SCARA Binary Wire Protocol Codec**: High-performance streaming frame parser, payload unpacker, frame builder, and CRC-16-CCITT integrity verification (``0xAA 0x55`` header framing).
* **Multi-Target Trajectory Exporter**: Export robotic trajectories into industrial G-code, CSV time-series data, JSON trajectory bundles, and SVG vector toolpaths.
* **Interactive Motion REPL Console**: Terminal-based interactive console (``scarac repl``) for real-time single-command compilation, inspection, and frame transmission.
* **Single Source of Truth (SSoT)**: Seamless domain and codec foundation shared between ``scarajectory`` (Desktop Studio), ``scaraemu`` (Digital Twin Simulator), and ``dof2bot/scara`` (RP2040 firmware).
* **Zero GUI Dependencies**: 100% headless, clean architecture design with zero Tkinter, Qt, or graphics dependencies.
* **Strict Quality & SOLID Standards**: 100% structural protocol conformance, 100% test coverage, and 10.00 / 10.00 Pylint score.
* **Resilient Error Handling & Categorized Diagnostics**: Strongly typed domain exception hierarchy (``ScaraSyntaxError``, ``ScaraSemanticError``, ``ScaraKinematicsError``, ``ScaraProtocolError``, ``ScaraExportError``, ``ScaraIOError``) coupled with dedicated CLI error presentation handlers (``ICompileErrorHandler``, ``IDecompileErrorHandler``, ``IDisassembleErrorHandler``, ``IExportErrorHandler``, ``ILintErrorHandler``) providing clear, category-tagged diagnostics (``[SYNTAX]``, ``[SEMANTIC]``, ``[KINEMATICS]``, ``[PROTOCOL]``, ``[EXPORT]``, ``[IO]``, ``[DOMAIN]``) and zero unhandled tracebacks at the system boundary.

📜 SCARA Domain-Specific Language (DSL) & ``.scara`` Programs
--------------------------------------------------------------------------------

**scaralang** includes a dedicated, industrial-grade Domain-Specific Language designed specifically for SCARA robotic manipulators. Programs are written in plain text files with the ``.scara`` extension and compiled into validated Cartesian trajectories via a clean AST pipeline, with full bidirectional decompilation back from binary bytecode:

.. code-block:: text

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

Dead Zone Avoidance & Safe Trajectory Routing Pipeline
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When generating continuous trajectories or executing Cartesian linear moves (``MOVE_L``), paths that intersect the inner annular physical dead zone (:math:`R_{\min} \approx 77.6\text{ mm}` for default SCARA geometry) are automatically detected and rerouted via tangent arc geometry:

.. code-block:: text

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

Verification Scripts & Examples (``examples/`` & ``run.sh``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The repository includes a comprehensive test and validation suite in ``examples/`` covering all motion primitives, coordinate frames, macro operations, and pneumatic controls:

.. list-table:: Industrial Verification Suite
   :widths: 30 40 30
   :header-rows: 1

   * - Script
     - Domain Feature
     - Output Artifacts
   * - ``01_homing.scara``
     - Multi-axis homing sequence
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``02_linear_motion.scara``
     - Linear Cartesian path interpolation (``MOVE_L``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``03_joint_rapid.scara``
     - Rapid joint point-to-point motion (``MOVE_J``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``04_circular_arc.scara``
     - Clockwise / counter-clockwise arcs (``ARC_CW`` / ``ARC_CCW``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``05_jump_arch.scara``
     - Parabolic arch pick-and-place transfer (``JUMP``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``06_pneumatics.scara``
     - End-effector vacuum pump & blow-off valve control
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``07_approach_retract.scara``
     - Vertical tool descent and safe retract (``APPROACH`` / ``RETRACT``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``08_work_frames.scara``
     - Workpiece coordinate frame offsets (``FRAME USER`` / ``FRAME BASE``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``09_pallet_matrix.scara``
     - Grid pallet matrix indexing (``PALLET_DEF`` / ``MOVE_PALLET``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``10_tangent_orientation.scara``
     - Automatic 4th-axis tool yaw tangent orientation
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``11_zone_blending.scara``
     - Corner tolerance continuous path smoothing (``ZONE``)
     - ``.bin``, ``.dis``, ``_decompiled.scara``
   * - ``12_industrial_pick_place.scara``
     - Complete industrial assembly & palletizing cycle
     - ``.bin``, ``.dis``, ``_decompiled.scara``

To validate compilation, decompiler round-trip, and disassembly across all examples in a single pass:

.. code-block:: bash

    # Execute automated batch compiler / decompiler verification
    bash run.sh

📡 SCARA Binary Wire Protocol & Codec
--------------------------------------------------------------------------------

All binary wire communication between **scaralang**, **scarajectory**, **scaraemu**, and physical robot firmware is governed by deterministic packet framing:

Frame Header & Wire Format
^^^^^^^^^^^^^^^^^^^^^^^^^^

Each binary wire frame consists of a 5-byte header, variable payload (0 to 64 bytes), and a 3-byte trailer (CRC-16-CCITT and EOF delimiter ``0x0D``):

.. code-block:: text

    ┌──────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────────┬──────────────┬──────────────┐
    │  SOF1 (0xAA) │  SOF2 (0x55) │  Msg ID (1B) │   SEQ (1B)   │  Length (1B) │   Payload (NB)   │  CRC16 (2B)  │  EOF (0x0D)  │
    └──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────────┴──────────────┴──────────────┘
    │<─────────────── 5-Byte Wire Header ──────────────────────>│  0..64 Bytes │<───── 3-Byte Wire Trailer ──────>│

Message Types & Payload Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: Binary Message Types
   :widths: 12 25 38 25
   :header-rows: 1

   * - Message ID
     - Enum Identifier
     - Payload Structure
     - Description
   * - ``0x01``
     - ``CMD_MOVE_JOINT_STEPS``
     - ``j1..j4 (16B), duration_us (4B), feed (2B)`` (22B)
     - Coordinated stepper motor joint step block with duration and feedrate.
   * - ``0x03``
     - ``CMD_ENABLE``
     - Empty (``0 bytes``)
     - Energize stepper motor driver stages (holding torque).
   * - ``0x04``
     - ``CMD_DISABLE``
     - Empty (``0 bytes``)
     - De-energize motor driver stages (free movement).
   * - ``0x05``
     - ``CMD_ESTOP``
     - Empty (``0 bytes``)
     - Immediate hardware emergency stop and motion abort.
   * - ``0x06``
     - ``CMD_HOME``
     - Empty (``0 bytes``)
     - Execute multi-axis homing sequence (Z -> J2 -> J1).
   * - ``0x07``
     - ``CMD_HOLD``
     - Empty (``0 bytes``)
     - Trajectory feed hold / pause motion execution.
   * - ``0x08``
     - ``CMD_RESUME``
     - Empty (``0 bytes``)
     - Resume suspended motion execution.
   * - ``0x09``
     - ``CMD_JOG_JOINT``
     - ``joint_id (1B), dir (1B), steps (2B)`` (4B)
     - Incremental single joint rotational/linear jog.
   * - ``0x0A``
     - ``CMD_SETPOS_STEPS``
     - ``s1, s2, s3, s4 (16B)``
     - Force absolute step register position without motion.
   * - ``0x0B``
     - ``CMD_TOOL_PUMP``
     - ``tool_id (1B), state (1B)`` (2B)
     - Vacuum suction pump actuation (``ON``/``OFF``).
   * - ``0x0C``
     - ``CMD_TOOL_VALVE``
     - ``tool_id (1B), state (1B)`` (2B)
     - Pneumatic blow-off release valve actuation (``ON``/``OFF``).
   * - ``0x0D``
     - ``CMD_WAIT``
     - ``delay_ms (4B)``
     - Dwell delay execution for specified milliseconds.
   * - ``0x0E``
     - ``CMD_OVERRIDE``
     - ``percent (1B: 10..200)``
     - Dynamically scale path execution velocity in real time.
   * - ``0x0F``
     - ``CMD_CONFIG_MOTOR``
     - ``motor_mode (1B), axis_mask (1B)`` (2B)
     - Select open-loop TMC2209 or closed-loop MKS SERVO42D.
   * - ``0x20``
     - ``CMD_GET_STATUS``
     - Empty (``0 bytes``)
     - Query consolidated robot status and motion flags.
   * - ``0x21``
     - ``CMD_GET_STEPS``
     - Empty (``0 bytes``)
     - Query current absolute joint step counters.
   * - ``0x22``
     - ``CMD_GET_DIAGNOSTICS``
     - Empty (``0 bytes``)
     - Query extended controller diagnostics and memory stats.
   * - ``0x23``
     - ``CMD_CLEAR_FAULT``
     - Empty (``0 bytes``)
     - Reset latched hardware fault condition.
   * - ``0x24``
     - ``CMD_PING``
     - ``timestamp_ms (4B)``
     - Real-time link health and latency measurement ping.
   * - ``0x30``
     - ``CMD_BOOTLOADER``
     - Empty (``0 bytes``)
     - Reboot controller into USB BOOTSEL firmware update mode.
   * - ``0x80``
     - ``RESP_ACK``
     - ``acked_id (1B), q_count (1B)`` (2B)
     - Positive command acknowledgment from robot controller.
   * - ``0x81``
     - ``RESP_NACK``
     - ``rejected_id (1B), error_code (1B)`` (2B)
     - Negative command rejection with hardware error code.
   * - ``0x82``
     - ``RESP_STATUS``
     - ``state, substate, flags (3B), s1..s4 (16B)`` (19B)
     - Real-time consolidated robot status and coordinates.
   * - ``0x83``
     - ``RESP_STEPS``
     - ``s1, s2, s3, s4 (16B)``
     - Current absolute joint step positions for all 4 axes.
   * - ``0x84``
     - ``RESP_PONG``
     - ``echo_timestamp_ms (4B)``
     - Heartbeat keepalive reply with round-trip timestamp.
   * - ``0x85``
     - ``RESP_MOVE_EVENT``
     - ``event_type (1B), step_index (4B)`` (5B)
     - Trajectory waypoint start/complete execution notification.
   * - ``0x86``
     - ``RESP_HOMING_EVENT``
     - ``axis_mask (1B), status (1B)`` (2B)
     - Multi-axis limit switch trigger event notification.
   * - ``0x88``
     - ``RESP_DIAGNOSTICS``
     - Extended 56-byte payload
     - System diagnostics (CPU, free RAM, temperature, drops).
   * - ``0x89``
     - ``RESP_FAULT_EVENT``
     - ``fault_code (2B), axis (1B), info (1B)`` (4B)
     - Critical hardware fault alert.

Hardware Execution & Motor Actuation Targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Binary wire frames generated by **scaralang** stream directly over UART / USB-CDC to the physical **``scara_base``** firmware running on the Raspberry Pi Pico (RP2040), which coordinates motor actuation across two configurable drive modes:

* **Open-Loop Stepper Mode (TMC2209):** Coordinated microstepping pulses generated by RP2040 PIO hardware state machines driving TMC2209 STEP/DIR stages for ultra-silent operation.
* **Closed-Loop Stepper Mode (MKS SERVO42D over CAN Bus):** NEMA stepper motors equipped with **MKS SERVO42D** closed-loop modules communicating with the Raspberry Pi Pico over a high-speed differential **CAN bus** (CAN_H / CAN_L). This guarantees 100% elimination of lost steps, hardware PID closed-loop position correction, and real-time following-error telemetry.

🛡️ Error Handling & Diagnostic Architecture
--------------------------------------------------------------------------------

**scaralang** implements end-to-end, resilient error handling and structured diagnostic reporting based on Clean Architecture principles. It enforces a strict separation between domain-level error contracts, core application validation, and presentation-layer error formatting.

Domain Exception Hierarchy
^^^^^^^^^^^^^^^^^^^^^^^^^^

All internal toolchain exceptions inherit from the base domain exception ``ScaraError`` (defined in ``scaralang.core.model.exceptions.scara_error``):

.. code-block:: text

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

.. list-table:: Domain Exception Hierarchy
   :widths: 22 38 12 28
   :header-rows: 1

   * - Exception Class
     - Module
     - Category
     - Description
   * - ``ScaraError``
     - ``core/model/exceptions/scara_error.py``
     - ``[DOMAIN]``
     - Base class for all domain, compiler, and protocol exceptions.
   * - ``ScaraSyntaxError``
     - ``core/model/exceptions/scara_syntax_error.py``
     - ``[SYNTAX]``
     - Lexer, tokenization, or parser grammar violations.
   * - ``ScaraSemanticError``
     - ``core/model/exceptions/scara_semantic_error.py``
     - ``[SEMANTIC]``
     - Semantic validation failures (undefined pallet, duplicate definitions).
   * - ``ScaraKinematicsError``
     - ``core/model/exceptions/scara_kinematics_error.py``
     - ``[KINEMATICS]``
     - Robot workspace, reachability, or mechanical singularity violations.
   * - ``ScaraProtocolError``
     - ``core/model/exceptions/scara_protocol_error.py``
     - ``[PROTOCOL]``
     - Wire framing, CRC-16 checksum failure, or truncated payload faults.
   * - ``ScaraExportError``
     - ``core/model/exceptions/scara_export_error.py``
     - ``[EXPORT]``
     - Trajectory export format errors or unsupported targets.
   * - ``ScaraIOError``
     - ``core/model/exceptions/scara_io_error.py``
     - ``[IO]``
     - File system access failures, missing input files, or permission faults.

Dedicated Command Error Handlers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In accordance with the Single Responsibility Principle (SRP) and Interface Segregation Principle (ISP), each CLI subcommand delegates error categorization, return code determination, and error formatting to a dedicated error handler:

.. list-table:: Dedicated Command Error Handlers
   :widths: 15 25 30 30
   :header-rows: 1

   * - Subcommand
     - Protocol Interface
     - Concrete Handler
     - Companion Factory
   * - ``compile``
     - ``ICompileErrorHandler``
     - ``CompileErrorHandler``
     - ``CompileErrorHandlerFactory``
   * - ``decompile``
     - ``IDecompileErrorHandler``
     - ``DecompileErrorHandler``
     - ``DecompileErrorHandlerFactory``
   * - ``disassemble``
     - ``IDisassembleErrorHandler``
     - ``DisassembleErrorHandler``
     - ``DisassembleErrorHandlerFactory``
   * - ``export``
     - ``IExportErrorHandler``
     - ``ExportErrorHandler``
     - ``ExportErrorHandlerFactory``
   * - ``lint``
     - ``ILintErrorHandler``
     - ``LintErrorHandler``
     - ``LintErrorHandlerFactory``

Categorized Diagnostics & Formatted Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a command fails, the corresponding error handler captures the domain exception, formats a category-tagged diagnostic message, and sets ``returncode = 1`` without unhandled tracebacks:

* **Syntax Errors (``[SYNTAX]``):**

  .. code-block:: bash

      $ scarac compile --script invalid_syntax.scara
      [SYNTAX] Line 4: Invalid float literal for parameter 'X': '150.abc'

* **Semantic Errors (``[SEMANTIC]``):**

  .. code-block:: bash

      $ scarac compile --script invalid_pallet.scara
      [SEMANTIC] Line 12: Referenced pallet 'TRAY1' has not been defined

* **Kinematics Violations (``[KINEMATICS]``):**

  .. code-block:: bash

      $ scarac compile --script out_of_reach.scara
      [KINEMATICS] Target coordinates (500.0, 300.0) exceed maximum reach of SCARA arm

* **Wire Protocol & Deserialization Errors (``[PROTOCOL]``):**

  .. code-block:: bash

      $ scarac decompile --file corrupted.bin
      [PROTOCOL] Payload truncated: expected 22 bytes for JOINT_STEPS, got 14 bytes

* **Export Target Errors (``[EXPORT]``):**

  .. code-block:: bash

      $ scarac export --script program.scara --format unsupported --output out.bin
      [EXPORT] Unsupported export format 'unsupported'

* **File System / Missing Input Errors (``[IO]``):**

  .. code-block:: bash

      $ scarac compile --script missing.scara
      compile::execute - file not found: missing.scara

Python Library API: Error Handling Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Downstream applications can catch specific domain exceptions for fine-grained error recovery:

.. code-block:: python

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

Python Library API
^^^^^^^^^^^^^^^^^^

.. code-block:: python

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