# SCARA Domain-Specific Language (DSL) Specification & Reference Manual

**Version:** 1.1.0  
**Target:** Industrial SCARA Robotic Manipulators  
**Toolchain:** `scaralang` (`scarac` compiler, decompiler & binary protocol engine)  
**Author:** Vladimir Roncevic  
**License:** GPL-3.0 / Apache-2.0  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Lexical Structure & Syntax](#2-lexical-structure--syntax)
   - [2.1 Line-Oriented Statements](#21-line-oriented-statements)
   - [2.2 Case Insensitivity](#22-case-insensitivity)
   - [2.3 Parameter Passing Styles](#23-parameter-passing-styles)
   - [2.4 Comments and Whitespace](#24-comments-and-whitespace)
   - [2.5 Coordinate System & Standard Units](#25-coordinate-system--standard-units)
3. [Language Instructions Reference](#3-language-instructions-reference)
   - [Category 1: Cartesian & Joint Motion](#category-1-cartesian--joint-motion)
     - [`MOVE_J`](#move_j) — Rapid Joint Point-to-Point Motion
     - [`MOVE_L`](#move_l) — Linear Cartesian Interpolated Motion
     - [`MOVE_REL`](#move_rel) — Relative Cartesian Incremental Motion
     - [`ARC_CW`](#arc_cw) — Clockwise Circular Arc Interpolation
     - [`ARC_CCW`](#arc_ccw) — Counter-Clockwise Circular Arc Interpolation
     - [`APPROACH`](#approach) — Relative Vertical Descent
     - [`RETRACT`](#retract) — Relative Vertical Ascent
     - [`JOG_AXIS`](#jog_axis) — Manual Incremental Cartesian Jog
     - [`JOG_JOINT`](#jog_joint) — Manual Incremental Joint Jog
     - [`PROBE`](#probe) — Tactile Surface Search
   - [Category 2: High-Level Macros, Subroutines & Spatial Zones](#category-2-high-level-macros-subroutines--spatial-zones)
     - [`JUMP`](#jump) — 3D Parabolic Arch Pick & Place
     - [`PALLET_DEF`](#pallet_def) — Matrix Pallet Grid Definition
     - [`MOVE_PALLET`](#move_pallet) — Pallet Index Positioning
     - [`DEF` / `END`](#def--end) — User-Defined Subroutine Routine
     - [`CALL`](#call) — Subroutine Invocation
     - [`REPEAT` / `END`](#repeat--end) — Fixed-Count Iteration Loop
     - [`ZONE_DEF`](#zone_def) — User-Defined Spatial Keep-Out Zone
   - [Category 3: Actuator & Tool Control](#category-3-actuator--tool-control)
     - [`PUMP`](#pump) — Vacuum Generator Actuation
     - [`VALVE`](#valve) — Vacuum Blow-Off Release Valve
     - [`TOOL`](#tool) — Vertical Slide Stage Actuation
     - [`TOOL_ORIENT`](#tool_orient) — End-Effector Orientation Mode
   - [Category 4: Dynamics & Trajectory Shaping](#category-4-dynamics--trajectory-shaping)
     - [`SPEED`](#speed) — Travel and Working Feedrate Limit
     - [`ACCEL`](#accel) — Path Acceleration Limit
     - [`OVERRIDE`](#override) — Dynamic Real-Time Speed Override
     - [`ZONE`](#zone) — Corner Path Blending & Rounding Mode
   - [Category 5: Work Coordinates & Kinematic Configuration](#category-5-work-coordinates--kinematic-configuration)
     - [`CONFIG ELBOW`](#config-elbow) — Kinematic Arm Solution Branch
     - [`CONFIG MOTOR`](#config-motor) — Stepper Drive Feedback Mode
     - [`FRAME_SET` / `FRAME`](#frame_set--frame) — Work Coordinate System (WCS)
     - [`FRAME_RESET`](#frame_reset) — Reset Coordinate System to World Base
     - [`HOME`](#home) — Multi-Axis Calibration & Homing Routine
   - [Category 6: Execution Flow & Safety](#category-6-execution-flow--safety)
     - [`WAIT` / `WAIT_MS`](#wait--wait_ms) — Trajectory Dwell Delay
     - [`SYNC`](#sync) — Trajectory Buffer Barrier Flush
     - [`HOLD`](#hold) — Trajectory Feed Hold (Pause)
     - [`RESUME`](#resume) — Resume Paused Trajectory
     - [`ESTOP`](#estop) — Immediate Emergency Stop
     - [`ENABLE`](#enable) — Energize Motor Driver Stages
     - [`DISABLE`](#disable) — De-energize Motor Driver Stages
4. [Static Analysis & Linter Rules](#4-static-analysis--linter-rules)
   - [4.1 Motion Rules](#41-motion-rules)
   - [4.2 Pneumatic & Vacuum Rules](#42-pneumatic--vacuum-rules)
   - [4.3 State & Kinematic Rules](#43-state--kinematic-rules)
   - [4.4 Timing & Blending Rules](#44-timing--blending-rules)
   - [4.5 Spatial Safety & Obstacle Collision Rules](#45-spatial-safety--obstacle-collision-rules)
5. [Examples Directory & Verification Artifacts](#5-examples-directory--verification-artifacts)
   - [5.1 Directory Structure & Artifact Types](#51-directory-structure--artifact-types)
   - [5.2 Comprehensive Examples Catalog](#52-comprehensive-examples-catalog)
   - [5.3 Toolchain CLI Workflows (Compile, Disassemble, Decompile)](#53-toolchain-cli-workflows-compile-disassemble-decompile)
6. [Complete Industrial Example Scripts](#6-complete-industrial-example-scripts)
   - [6.1 High-Speed Pick and Place with Matrix Pallet](#61-high-speed-pick-and-place-with-matrix-pallet)
   - [6.2 Circular Profiling with Tool Tangency](#62-circular-profiling-with-tool-tangency)
   - [6.3 Surface Probing and Adhesive Dispensing](#63-surface-probing-and-adhesive-dispensing)

---

## 1. Introduction

The **SCARA Domain-Specific Language (DSL)** is a high-level, human-readable robotic programming language designed specifically for Selective Compliance Assembly Robot Arm (SCARA) 4-axis manipulators ($X, Y, Z, \Phi$).

Unlike generic CNC G-code, SCARA DSL is natively aware of:
- **Kinematic arm configurations** (Elbow Left vs. Elbow Right branch solutions).
- **Robotic pick-and-place abstractions** (smooth 3D parabolic `JUMP` arches, pallet matrix generation, rapid approach/retract moves).
- **Integrated pneumatic end-effector management** (vacuum suction cup, blow-off release valve, vertical slide).
- **Dynamic motion blending zones** (fly-by corner rounding for continuous trajectory execution).
- **Deterministic bytecode compilation** directly into packed binary stepper motor execution frames (`0xAA 0x55` wire protocol).

---

## 2. Lexical Structure & Syntax

### 2.1 Line-Oriented Statements

A `.scara` program consists of sequence lines. Each line contains at most one statement. A statement starts with a command keyword, followed by optional or required parameters:

```scara
MOVE_L X 150.0 Y 45.0 Z 20.0
PUMP ON
WAIT 150
```

### 2.2 Case Insensitivity

All command keywords and parameter identifiers are case-insensitive:

```scara
MOVE_L X 100.0 Y 50.0 Z 10.0
move_l x 100.0 y 50.0 z 10.0
Move_L X 100.0 Y 50.0 Z 10.0
```
All three variants produce identical AST nodes and binary instructions.

### 2.3 Parameter Passing Styles

Parameters may be passed either using whitespace separation (`KEY VALUE`) or explicit assignment (`KEY=VALUE`):

```scara
# Whitespace style
MOVE_L X 150.0 Y 75.0 Z 20.0 P 45.0

# Assignment style
MOVE_L X=150.0 Y=75.0 Z=20.0 P=45.0

# Mixed style (fully supported)
JUMP X 150.0 Y=75.0 Z 20.0 ARCH=35.0
```

### 2.4 Comments and Whitespace

- Single-line comments begin with `#` or `;` and extend to the end of the line:
  ```scara
  # This is a comment
  SPEED WORK 80.0   ; Set working feedrate to 80 mm/s
  ```
- Blank lines and redundant whitespace (leading, trailing, internal spaces, tabs) are ignored by the lexer.

### 2.5 Coordinate System & Standard Units

| Dimension | Axis | Unit | Description |
|---|---|---|---|
| Linear Coordinates | `X`, `Y`, `Z` | Millimeters (`mm`) | Absolute or frame-relative Cartesian position. |
| Tool Orientation | `P` / `PHI` | Degrees (`°`) | 4th-axis end-effector yaw rotation ($\pm 180^\circ$). |
| Arc Center Offsets | `I`, `J` | Millimeters (`mm`) | Incremental vector offset from starting point to arc center. |
| Feedrate | `SPEED` | `mm/s` | Tool center point (TCP) linear speed. |
| Acceleration | `ACCEL` | `mm/s²` | Linear path acceleration and deceleration. |
| Time Delay | `WAIT` / `WAIT_MS` | Milliseconds (`ms`) | Hardware execution dwell. |
| Joint Angles | `deg` | Degrees (`°`) | Joint 1, Joint 2 arm angles, Joint 4 yaw. |

---

## 3. Language Instructions Reference

### Category 1: Cartesian & Joint Motion

---

#### `MOVE_J`
**Rapid Joint Point-to-Point Motion**

Moves the robot arm to the target Cartesian coordinates using non-interpolated joint motion. Both arm joints articulate simultaneously at maximum speed without enforcing a straight-line Cartesian path. Best used for clearance travel and rapid repositioning.

- **Syntax:** `MOVE_J X <x> Y <y> Z <z> [P <phi>]`
- **Parameters:**
  - `X`: *float (mm)* — Target X coordinate.
  - `Y`: *float (mm)* — Target Y coordinate.
  - `Z`: *float (mm)* — Target Z coordinate.
  - `P` / `PHI`: *float (deg, optional)* — Target tool orientation angle.
- **Example:**
  ```scara
  MOVE_J X 150.0 Y -50.0 Z 40.0 P 0.0
  ```

---

#### `MOVE_L`
**Linear Cartesian Interpolated Motion**

Executes a linear, straight-line trajectory from the current position to the destination coordinates at the currently active working feedrate (`SPEED WORK`).

- **Syntax:** `MOVE_L X <x> Y <y> Z <z> [P <phi>]`
- **Parameters:**
  - `X`: *float (mm)* — Target X coordinate.
  - `Y`: *float (mm)* — Target Y coordinate.
  - `Z`: *float (mm)* — Target Z coordinate.
  - `P` / `PHI`: *float (deg, optional)* — Target tool orientation angle.
- **Example:**
  ```scara
  MOVE_L X 180.0 Y 60.0 Z 15.0 P 90.0
  ```

---

#### `MOVE_REL`
**Relative Cartesian Incremental Motion**

Executes an incremental straight-line Cartesian motion relative to the current tool pose. Incremental offsets ($\Delta X, \Delta Y, \Delta Z, \Delta \Phi$) are applied in the currently active coordinate work frame.

- **Syntax:** `MOVE_REL [X <dx>] [Y <dy>] [Z <dz>] [P <dphi>] [SPEED <spd>]`
- **Parameters:**
  - `X`: *float (mm, optional)* — Relative displacement along X axis (default `0.0`).
  - `Y`: *float (mm, optional)* — Relative displacement along Y axis (default `0.0`).
  - `Z`: *float (mm, optional)* — Relative displacement along Z axis (default `0.0`).
  - `P` / `PHI`: *float (deg, optional)* — Relative rotation angle about tool axis (default `0.0`).
  - `SPEED`: *float (mm/s, optional)* — Target path velocity.
- **Example:**
  ```scara
  # Shift 20mm in X, 10mm in Y, and descend 5mm
  MOVE_REL X=20.0 Y=10.0 Z=-5.0 SPEED=40.0
  ```

---

#### `ARC_CW`
**Clockwise Circular Arc Interpolation**

Interpolates a circular arc in the XY plane in a clockwise direction. The arc begins at the current robot position and terminates at `(X, Y)`. The circle center is defined relative to the starting position via `I` (X offset) and `J` (Y offset).

- **Syntax:** `ARC_CW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]`
- **Parameters:**
  - `X`, `Y`: *float (mm)* — Arc endpoint coordinates.
  - `I`: *float (mm)* — Incremental X distance from start position to circle center.
  - `J`: *float (mm)* — Incremental Y distance from start position to circle center.
  - `Z`: *float (mm, optional)* — Helical motion target Z coordinate.
  - `P`: *float (deg, optional)* — Final tool orientation.
- **Example:**
  ```scara
  # Semi-circle of radius 25mm clockwise
  ARC_CW X 150.0 Y 50.0 I 0.0 J 25.0
  ```

---

#### `ARC_CCW`
**Counter-Clockwise Circular Arc Interpolation**

Interpolates a circular arc in the XY plane in a counter-clockwise direction from the current position to `(X, Y)` around the center offset `(I, J)`.

- **Syntax:** `ARC_CCW X <x> Y <y> I <i> J <j> [Z <z>] [P <p>]`
- **Parameters:**
  - `X`, `Y`: *float (mm)* — Arc endpoint coordinates.
  - `I`, `J`: *float (mm)* — Arc center vector offsets.
  - `Z`: *float (mm, optional)* — Optional helical vertical coordinate.
- **Example:**
  ```scara
  ARC_CCW X 100.0 Y 80.0 I -20.0 J 0.0
  ```

---

#### `APPROACH`
**Relative Vertical Descent**

Performs a relative vertical descent along the negative Z axis from the current position by the specified clearance distance. Used to move down safely from clearance plane to pickup or placement plane.

- **Syntax:** `APPROACH DIST <d>`
- **Parameters:**
  - `DIST`: *float (mm, > 0)* — Vertical descent distance.
- **Example:**
  ```scara
  APPROACH DIST 35.0
  ```

---

#### `RETRACT`
**Relative Vertical Ascent**

Performs a relative vertical ascent along the positive Z axis from the current position by the specified clearance distance. Used to lift the tool up safely away from workpiece and fixtures before horizontal moves.

- **Syntax:** `RETRACT DIST <d>`
- **Parameters:**
  - `DIST`: *float (mm, > 0)* — Vertical ascent distance.
- **Example:**
  ```scara
  RETRACT DIST 35.0
  ```

---

#### `JOG_AXIS`
**Manual Incremental Cartesian Jog**

Commands a single-axis relative jog displacement along a chosen Cartesian degree of freedom. Used primarily in manual setup, calibration, and REPL control.

- **Syntax:** `JOG_AXIS <X|Y|Z|PHI> <step>`
- **Parameters:**
  - Axis identifier: `X`, `Y`, `Z`, or `PHI`.
  - `step`: *float* — Distance in mm (or degrees for PHI) to step.
- **Example:**
  ```scara
  JOG_AXIS X 5.0
  JOG_AXIS Z -1.0
  JOG_AXIS PHI 15.0
  ```

---

#### `JOG_JOINT`
**Manual Incremental Joint Jog**

Rotates an individual robotic actuator joint by a relative angle.

- **Syntax:** `JOG_JOINT <joint_id> <deg>`
- **Parameters:**
  - `joint_id`: *int (1 to 4)* — Joint 1 (Base shoulder), Joint 2 (Elbow), Joint 3 (Z axis), Joint 4 (Wrist yaw).
  - `deg`: *float* — Relative rotation in degrees (or mm for linear Z joint 3).
- **Example:**
  ```scara
  JOG_JOINT 1 10.0
  JOG_JOINT 2 -5.5
  ```

---

#### `PROBE`
**Tactile Surface Search**

Drives the Z-axis downwards at a controlled speed until a tactile touch probe or microswitch sensor triggers. Upon contact, the current coordinate is registered, motion halts cleanly, and subsequent commands proceed from the probed plane.

- **Syntax:** `PROBE [SPEED <s>] [DIST <d>]`
- **Parameters:**
  - `SPEED`: *float (mm/s, optional)* — Search velocity (default: 10 mm/s).
  - `DIST`: *float (mm, optional)* — Maximum search travel distance.
- **Example:**
  ```scara
  PROBE SPEED 5.0 DIST 40.0
  ```

---

### Category 2: High-Level Macros, Subroutines & Spatial Zones

---

#### `JUMP`
**3D Parabolic Arch Pick & Place**

The quintessential robotic pick-and-place command. Expands into a smooth, time-optimal 3D motion consisting of:
1. Smooth vertical lift-off along Z to apex height `ARCH`.
2. High-speed horizontal transfer in XY plane.
3. Smooth vertical descent to destination `(X, Y, Z)`.

Eliminates discrete corner stops and optimizes cycle times.

- **Syntax:** `JUMP X <x> Y <y> Z <z> [ARCH <h> | ARCH_HEIGHT <h>]`
- **Parameters:**
  - `X`, `Y`, `Z`: *float (mm)* — Destination coordinates.
  - `ARCH` / `ARCH_HEIGHT`: *float (mm, optional)* — Height of arch apex above the higher of source or target Z (default: 25.0 mm).
- **Example:**
  ```scara
  JUMP X 220.0 Y 45.0 Z 10.0 ARCH 35.0
  ```

---

#### `PALLET_DEF`
**Matrix Pallet Grid Definition**

Defines a structured 2D Cartesian pallet matrix of components or trays. Establishes the grid layout with row count, column count, and pitch offsets between cells.

- **Syntax:** `PALLET_DEF <name> ROWS <r> COLS <c> DX <dx> DY <dy> [Z <z>] [P <p>]`
- **Parameters:**
  - `name`: *string* — Unique identifier for the pallet grid.
  - `ROWS`: *int* — Number of rows in the pallet grid.
  - `COLS`: *int* — Number of columns in the pallet grid.
  - `DX`: *float (mm)* — Pitch spacing between adjacent columns along X.
  - `DY`: *float (mm)* — Pitch spacing between adjacent rows along Y.
  - `Z`: *float (mm, optional)* — Default pallet working plane height.
  - `P`: *float (deg, optional)* — Default component orientation.
- **Example:**
  ```scara
  PALLET_DEF TRAY1 ROWS 4 COLS 6 DX 20.0 DY 25.0 Z 12.0
  ```

---

#### `MOVE_PALLET`
**Pallet Index Positioning**

Moves the robot to the specified 1-indexed cell within a previously defined pallet matrix. Automatically computes the Cartesian coordinates based on row and column index.

- **Syntax:** `MOVE_PALLET <name> INDEX <i>`
- **Parameters:**
  - `name`: *string* — Name of previously defined pallet.
  - `INDEX`: *int (1 to ROWS*COLS)* — 1-based sequential slot index.
- **Example:**
  ```scara
  MOVE_PALLET TRAY1 INDEX 7
  APPROACH DIST 15.0
  PUMP ON
  ```

---

#### `DEF` / `END`
**User-Defined Subroutine Definition**

Declares a reusable, parameterized routine block consisting of high-level SCARA instructions. The routine is registered into the AST symbol table and expanded inline upon invocation with nested block support.

- **Syntax:**
  ```scara
  DEF <name>
      <instructions>
  END
  ```
- **Parameters:**
  - `name`: *string* — Unique identifier for the subroutine.
- **Example:**
  ```scara
  DEF PICK_PART
      APPROACH DIST 25.0
      PUMP ON
      WAIT 100
      RETRACT DIST 25.0
  END
  ```

---

#### `CALL`
**Subroutine Invocation**

Invokes a previously declared user subroutine by name. Expands into the defined sequence of instructions during the macro compilation phase.

- **Syntax:** `CALL <name>`
- **Parameters:**
  - `name`: *string* — Identifier of the defined subroutine to execute.
- **Example:**
  ```scara
  CALL PICK_PART
  ```

---

#### `REPEAT` / `END`
**Fixed-Count Iteration Loop**

Executes an enclosed block of SCARA instructions for a specified number of repetitions. Loops can be nested and support incremental relative motions, pallet advances, and sensor sampling.

- **Syntax:**
  ```scara
  REPEAT COUNT <n>
      <instructions>
  END
  ```
- **Parameters:**
  - `COUNT`: *int* — Number of iterations to execute ($N \ge 1$).
- **Example:**
  ```scara
  REPEAT COUNT 4
      MOVE_REL X 10.0 Y 0.0 Z 0.0
      TOOL DOWN
      WAIT 50
      TOOL UP
  END
  ```

---

#### `ZONE_DEF`
**User-Defined Spatial Keep-Out Zone**

Declares a geometric forbidden keep-out obstacle zone (rectangular bounding box or 2D circular boundary) in the robot's Cartesian workspace. During compilation and linting, the static obstacle collision checker verifies all trajectory segments (linear, joint, and circular arcs) against declared zones, reporting `OBSTACLE_COLLISION` errors before hardware transmission.

- **Syntax (Rectangular Box):**
  `ZONE_DEF <id> BOX X_MIN <x1> X_MAX <x2> Y_MIN <y1> Y_MAX <y2>`
- **Syntax (Circular Cylinder):**
  `ZONE_DEF <id> CIRCLE CENTER_X <cx> CENTER_Y <cy> RADIUS <r>`
- **Parameters:**
  - `id`: *string* — Unique identifier for the spatial obstacle zone.
  - `BOX`: Declares rectangular boundary where $X_{min} < X_{max}$ and $Y_{min} < Y_{max}$.
  - `CIRCLE`: Declares circular boundary where $R > 0$.
- **Example:**
  ```scara
  ZONE_DEF POST1 BOX X_MIN 120.0 X_MAX 140.0 Y_MIN -20.0 Y_MAX 20.0
  ZONE_DEF TOWER CIRCLE CENTER_X 200.0 CENTER_Y 50.0 RADIUS 25.0
  ```

---

### Category 3: Actuator & Tool Control

---

#### `PUMP`
**Vacuum Generator Actuation**

Controls the vacuum suction generator pump for end-effector pneumatic pick-and-place grippers.

- **Syntax:** `PUMP <ON|OFF>`
- **Parameters:**
  - State: `ON` (energize vacuum generator) or `OFF` (cut vacuum).
- **Linter Rule:** The linter warns if `PUMP ON` is commanded while `VALVE ON` is active (pneumatic conflict), or if rapid motion occurs without an intervening `WAIT` to establish vacuum seal.
- **Example:**
  ```scara
  PUMP ON
  WAIT 150
  ```

---

#### `VALVE`
**Vacuum Blow-Off Release Valve**

Actuates the pneumatic release blow-off valve to exhaust vacuum pressure and instantaneously release gripped parts.

- **Syntax:** `VALVE <ON|OFF>`
- **Parameters:**
  - State: `ON` (open release valve) or `OFF` (close release valve).
- **Example:**
  ```scara
  PUMP OFF
  VALVE ON
  WAIT 80
  VALVE OFF
  ```

---

#### `TOOL`
**Vertical Slide Stage Actuation**

Controls a secondary high-speed pneumatic or motorized vertical slide stage mounted on the tool head.

- **Syntax:** `TOOL <UP|DOWN>`
- **Parameters:**
  - State: `UP` (retract tool head slide) or `DOWN` (extend tool head slide).
- **Example:**
  ```scara
  TOOL DOWN
  PUMP ON
  WAIT 100
  TOOL UP
  ```

---

#### `TOOL_ORIENT`
**End-Effector Orientation Mode**

Configures the 4th-axis tool yaw tracking behavior during multi-axis path execution.

- **Syntax:** `TOOL_ORIENT <AUTO|TANGENT|FIXED>`
- **Parameters:**
  - `AUTO`: Automatically computes orientation to match arm configuration.
  - `TANGENT`: Dynamically rotates the tool center point tangential to the travel path curve (vital for dispensing, cutting, and welding).
  - `FIXED`: Preserves constant world orientation regardless of arm kinematics.
- **Example:**
  ```scara
  TOOL_ORIENT TANGENT
  ```

---

### Category 4: Dynamics & Trajectory Shaping

---

#### `SPEED`
**Travel and Working Feedrate Limit**

Sets the maximum Cartesian linear velocity for subsequent motion segments. Supports separate definitions for rapid positioning (`RAPID`) and working contact travel (`WORK`).

- **Syntax:** `SPEED <RAPID|WORK> <feedrate>`
- **Parameters:**
  - Channel: `RAPID` or `WORK`.
  - `feedrate`: *float (mm/s, > 0)* — Linear velocity limit.
- **Example:**
  ```scara
  SPEED RAPID 250.0
  SPEED WORK 60.0
  ```

---

#### `ACCEL`
**Path Acceleration Limit**

Configures the maximum linear path acceleration and deceleration for trajectory planning.

- **Syntax:** `ACCEL <val>`
- **Parameters:**
  - `val`: *float (mm/s², > 0)* — Acceleration limit.
- **Example:**
  ```scara
  ACCEL 500.0
  ```

---

#### `OVERRIDE`
**Dynamic Real-Time Speed Override**

Applies a dynamic global percentage scaling factor to all path feedrates without modifying programmed velocity coordinates.

- **Syntax:** `OVERRIDE <percent>`
- **Parameters:**
  - `percent`: *int or float (10 to 200)* — Speed percentage (100 = 100% nominal speed).
- **Example:**
  ```scara
  OVERRIDE 80
  ```

---

#### `ZONE`
**Corner Path Blending & Rounding Mode**

Controls corner rounding and trajectory continuous path blending between adjacent motion segments.

- **Syntax:** `ZONE <OFF|FINE|EXACT|Z1..Z50>`
- **Parameters:**
  - `OFF` / `FINE` / `EXACT`: Decelerates to an exact full stop at the programmed waypoint before beginning the next segment (zero corner rounding).
  - `Z1` to `Z50`: Blends corners smoothly with a tolerance zone of 1mm to 50mm, preserving continuous velocity and cutting cycle times.
- **Example:**
  ```scara
  ZONE Z5
  MOVE_L X 100.0 Y 50.0 Z 20.0
  MOVE_L X 150.0 Y 100.0 Z 20.0
  ZONE EXACT
  ```

---

### Category 5: Work Coordinates & Kinematic Configuration

---

#### `CONFIG ELBOW`
**Kinematic Arm Solution Branch**

Specifies the inverse kinematics arm solution configuration. For any SCARA Cartesian coordinate within the workspace, two valid joint angles exist: Elbow Left or Elbow Right.

- **Syntax:** `CONFIG ELBOW <LEFT|RIGHT>`
- **Parameters:**
  - Branch: `LEFT` or `RIGHT`.
- **Linter Rule:** Switching elbow configuration in the middle of a continuous path triggers a linter error; re-configuration must take place when stationary.
- **Example:**
  ```scara
  CONFIG ELBOW RIGHT
  ```

---

#### `CONFIG MOTOR`
**Stepper Drive Feedback Mode**

Selects the actuation drive mode of the robot joint steppers.

- **Syntax:** `CONFIG MOTOR <OPEN_LOOP|CLOSED_LOOP>`
- **Parameters:**
  - Mode: `OPEN_LOOP` (standard microstepping) or `CLOSED_LOOP` (encoder closed-loop field-oriented control).
- **Example:**
  ```scara
  CONFIG MOTOR CLOSED_LOOP
  ```

---

#### `FRAME_SET` / `FRAME`
**Work Coordinate System (WCS)**

Defines a local User Coordinate System offset from the robot base. All subsequent motion coordinates are interpreted relative to this frame.

- **Syntax:** `FRAME X <x> Y <y> Z <z> [PHI <p>]` or `FRAME_SET X <x> Y <y> Z <z> [PHI <p>]`
- **Parameters:**
  - `X`, `Y`, `Z`: *float (mm)* — Origin translation vector from base world origin.
  - `PHI`: *float (deg, optional)* — Rotation angle of the work frame around Z.
- **Example:**
  ```scara
  FRAME X 100.0 Y 50.0 Z 0.0 PHI 30.0
  ```

---

#### `FRAME_RESET`
**Reset Coordinate System to World Base**

Clears all active work coordinate transformations, restoring the global robot base origin as the reference coordinate frame.

- **Syntax:** `FRAME_RESET`
- **Parameters:** None.
- **Example:**
  ```scara
  FRAME_RESET
  ```

---

#### `HOME`
**Multi-Axis Calibration & Homing Routine**

Executes the hardware reference homing sequence for all axes (Joint 1, Joint 2, Z-axis, Tool yaw). Synchronizes stepper motor step counters with optical physical limit switches.

- **Syntax:** `HOME`
- **Parameters:** None.
- **Linter Rule:** Any motion instruction executed before `HOME` produces a high-priority warning from `MotionCalibrationValidator`.
- **Example:**
  ```scara
  HOME
  ```

---

### Category 6: Execution Flow & Safety

---

#### `WAIT` / `WAIT_MS`
**Trajectory Dwell Delay**

Pauses program execution for a specified duration in milliseconds. Used to allow pneumatic pressures to equalize, mechanical vibrations to dampen, or peripheral automation to index.

- **Syntax:** `WAIT <ms>` or `WAIT_MS <ms>`
- **Parameters:**
  - `ms`: *int or float (>= 0)* — Dwell delay in milliseconds.
- **Example:**
  ```scara
  WAIT 200
  ```

---

#### `SYNC`
**Trajectory Buffer Barrier Flush**

Inserts an execution barrier that blocks further command execution until the robot controller's motion buffer completely drains and all axes come to a complete physical standstill.

- **Syntax:** `SYNC`
- **Parameters:** None.
- **Example:**
  ```scara
  SYNC
  ```

---

#### `HOLD`
**Trajectory Feed Hold (Pause)**

Commands a controlled deceleration and immediate suspension of the running trajectory. Motors remain energized and position coordinates are preserved.

- **Syntax:** `HOLD`
- **Parameters:** None.

---

#### `RESUME`
**Resume Paused Trajectory**

Resumes motion along a previously paused (`HOLD`) trajectory from the exact suspended coordinates.

- **Syntax:** `RESUME`
- **Parameters:** None.

---

#### `ESTOP`
**Immediate Emergency Stop**

Executes an instantaneous hard stop aborting all motion, clearing command queues, and locking execution until an explicit reset.

- **Syntax:** `ESTOP`
- **Parameters:** None.

---

#### `ENABLE`
**Energize Motor Driver Stages**

Powers up and energizes the stepper motor driver stages, applying holding torque to all axes.

- **Syntax:** `ENABLE`
- **Parameters:** None.

---

#### `DISABLE`
**De-energize Motor Driver Stages**

Cuts power to stepper driver motor windings, releasing holding torque. Allows manual positioning by hand.

- **Syntax:** `DISABLE`
- **Parameters:** None.

---

## 4. Static Analysis & Linter Rules

The `scaralang` toolchain includes an industrial-grade static analyzer and linter (`scarac lint`). It inspects AST instructions before compilation and flags semantic issues into three severity categories: `ERROR`, `WARNING`, and `INFO`.

### 4.1 Motion Rules

| Rule Identifier | Checker Service | Description | Severity |
|---|---|---|---|
| `MOTION_UNCALIBRATED` | `MotionCalibrationValidator` | Motion instruction (`MOVE_J`, `MOVE_L`, etc.) is commanded before `HOME` homing routine. | `WARNING` |
| `MOTION_DUPLICATE` | `MotionDuplicateValidator` | Adjacent move instructions specify identical target coordinates, wasting trajectory planning cycles. | `INFO` |
| `MOTION_WORKSPACE_LIMIT` | `TrajectoryValidator` | Target coordinate falls outside the physical reach envelope ($R_{min} \le r \le R_{max}$, $Z_{min} \le z \le Z_{max}$). | `ERROR` |

### 4.2 Pneumatic & Vacuum Rules

| Rule Identifier | Checker Service | Description | Severity |
|---|---|---|---|
| `PNEUMATIC_CONFLICT` | `PneumaticConflictValidator` | `PUMP ON` and `VALVE ON` are commanded simultaneously, causing hardware pneumatic contention. | `ERROR` |
| `PNEUMATIC_FLYBY` | `PneumaticFlybyValidator` | `PUMP ON` is triggered without a subsequent dwell (`WAIT`) before initiating rapid motion, risking part drop. | `WARNING` |
| `PNEUMATIC_REDUNDANT` | `PneumaticRedundancyValidator` | Consecutive redundant state changes (e.g. `PUMP ON` followed immediately by `PUMP ON`). | `INFO` |

### 4.3 State & Kinematic Rules

| Rule Identifier | Checker Service | Description | Severity |
|---|---|---|---|
| `STATE_HOMING_REDUNDANT` | `StateHomingValidator` | Multiple `HOME` commands placed without physical reason. | `INFO` |
| `STATE_MOTOR_MODE` | `MotorModeValidator` | Incompatible motor drive mode or configuration timing. | `WARNING` |
| `STATE_ZONE_CONFLICT` | `StateZoneValidator` | Zone rounding enabled during precision pick/place or probing sequences. | `WARNING` |

### 4.4 Timing & Blending Rules

| Rule Identifier | Checker Service | Description | Severity |
|---|---|---|---|
| `TIMING_DWELL_EXCESSIVE` | `TimingDwellValidator` | Single `WAIT` command exceeds 60,000 ms (1 minute), likely an error. | `WARNING` |
| `TIMING_BLEND_COLLISION` | `TimingBlendZoneValidator` | Corner blend zone radius is larger than the motion segment distance. | `ERROR` |

### 4.5 Spatial Safety & Obstacle Collision Rules

| Rule Identifier | Checker Service | Description | Severity |
|---|---|---|---|
| `OBSTACLE_COLLISION` | `ObstacleLintRule` | Trajectory path segment (linear, joint, or arc) intersects user-defined spatial keep-out obstacle zone (`ZONE_DEF`). | `ERROR` |

---

## 5. Examples Directory & Verification Artifacts

The [`examples/`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/) directory at the repository root contains 50 industrial test programs providing reference implementations for all categories of the SCARA DSL specification.

### 5.1 Directory Structure & Artifact Types

Every example program in [`examples/`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/) includes 4 artifact files validating round-trip toolchain compilation, binary wire framing, and decompilation:

| File Extension | Artifact Role | Description |
|---|---|---|
| `.scara` | **High-Level Source** | Original human-readable SCARA DSL script adhering to the language specification. |
| `.bin` | **Compiled Bytecode** | Packed binary execution payload framed with `0xAA 0x55` delimiter, message IDs, payload bytes, and CRC-16-CCITT checksums. |
| `.dis` | **Disassembly Inspection** | Frame-by-frame textual disassembly detailing wire sequence numbers, opcode IDs, payload unpacks, and hex bytes. |
| `_decompiled.scara` | **Decompiled Source** | Regenerated SCARA DSL script reverse-engineered directly from `.bin` by `scaralang decompile`. |

---

### 5.2 Comprehensive Examples Catalog

| # | Program Name | Primary Features & DSL Instructions | Source & Artifacts |
|---|---|---|---|
| **01** | Multi-Axis Homing | Multi-axis motor energizing, vertical slide homing, and coordinate origin calibration (`ENABLE`, `HOME`) | [`01_homing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/01_homing.scara)<br>[`01_homing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/01_homing.bin) |
| **02** | Cartesian Linear Motion | Coordinated straight-line Cartesian interpolation with feedrate limits (`MOVE_L`, `SPEED WORK`, `SPEED RAPID`) | [`02_linear_motion.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/02_linear_motion.scara)<br>[`02_linear_motion.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/02_linear_motion.bin) |
| **03** | Joint-Interpolated Rapid | Unconstrained multi-joint point-to-point rapid transit between fixtures (`MOVE_J`) | [`03_joint_rapid.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/03_joint_rapid.scara)<br>[`03_joint_rapid.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/03_joint_rapid.bin) |
| **04** | Circular Arc Interpolation | Planar arc interpolation with relative center offsets (`ARC_CW`, `ARC_CCW`, `I`, `J`) | [`04_circular_arc.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/04_circular_arc.scara)<br>[`04_circular_arc.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/04_circular_arc.bin) |
| **05** | 3D Parabolic Jump Arch | Industrial pick-and-place arch move with parameterized clearance height (`JUMP`, `ARCH`) | [`05_jump_arch.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/05_jump_arch.scara)<br>[`05_jump_arch.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/05_jump_arch.bin) |
| **06** | Pneumatics & Vacuum Control | Vacuum suction cup engagement, positive blow-off burst, and dwell settling (`PUMP`, `VALVE`, `WAIT_MS`) | [`06_pneumatics.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/06_pneumatics.scara)<br>[`06_pneumatics.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/06_pneumatics.bin) |
| **07** | Relative Approach & Retract | Controlled low-speed vertical descent and high-speed vertical ascent (`APPROACH`, `RETRACT`) | [`07_approach_retract.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/07_approach_retract.scara)<br>[`07_approach_retract.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/07_approach_retract.bin) |
| **08** | Work Coordinate Frames (WCS) | Named local coordinate frames, spatial origin shifts, and base reset (`FRAME_DEF`, `FRAME_SET`, `FRAME_RESET`) | [`08_work_frames.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/08_work_frames.scara)<br>[`08_work_frames.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/08_work_frames.bin) |
| **09** | Palletizing Matrix Grid | 2D matrix tray definition and zero-indexed cell positioning (`PALLET_DEF`, `MOVE_PALLET`) | [`09_pallet_matrix.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/09_pallet_matrix.scara)<br>[`09_pallet_matrix.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/09_pallet_matrix.bin) |
| **10** | Tangential Tool Orientation | Continuous 4th-axis yaw alignment tangential to trajectory path vector (`TOOL_ORIENT TANGENT`) | [`10_tangent_orientation.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/10_tangent_orientation.scara)<br>[`10_tangent_orientation.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/10_tangent_orientation.bin) |
| **11** | Corner Zone Blending | Fly-by corner rounding and exact stop transition blending (`ZONE EXACT`, `ZONE BLEND R=...`) | [`11_zone_blending.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/11_zone_blending.scara)<br>[`11_zone_blending.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/11_zone_blending.bin) |
| **12** | Industrial Pick & Place | Complete coordinated industrial pick-and-place workcell routine combining all subsystem capabilities | [`12_industrial_pick_place.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/12_industrial_pick_place.scara)<br>[`12_industrial_pick_place.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/12_industrial_pick_place.bin) |
| **13** | Elbow Reconfiguration | Dynamic elbow orientation switching (LEFT to RIGHT) with singularity clearance | [`13_elbow_reconfiguration.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/13_elbow_reconfiguration.scara)<br>[`13_elbow_reconfiguration.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/13_elbow_reconfiguration.bin) |
| **14** | Singularity Avoidance | Multi-tier singularity prevention and near-boundary damping | [`14_singularity_avoidance.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/14_singularity_avoidance.scara)<br>[`14_singularity_avoidance.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/14_singularity_avoidance.bin) |
| **15** | Boundary Reach Limits | Cartesian workspace envelop boundary verification and clamping | [`15_boundary_reach_limits.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/15_boundary_reach_limits.scara)<br>[`15_boundary_reach_limits.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/15_boundary_reach_limits.bin) |
| **16** | Multi-Frame Palletizing | Multiple work frame definitions with local pallet grid assembly | [`16_multi_frame_palletizing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/16_multi_frame_palletizing.scara)<br>[`16_multi_frame_palletizing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/16_multi_frame_palletizing.bin) |
| **17** | Bidirectional Assembly | Reconfiguration and bilateral pallet transfer across dual fixtures | [`17_bidirectional_elbow_assembly.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/17_bidirectional_elbow_assembly.scara)<br>[`17_bidirectional_elbow_assembly.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/17_bidirectional_elbow_assembly.bin) |
| **18** | Tangential Dispensing | Smooth glue bead dispensing with continuous tangential tool orientation | [`18_tangential_contour_dispensing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/18_tangential_contour_dispensing.scara)<br>[`18_tangential_contour_dispensing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/18_tangential_contour_dispensing.bin) |
| **19** | High-Speed Sorter Jump | Fast parabolic jump gate pick-and-place with velocity tuning | [`19_high_speed_sorter_jump.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/19_high_speed_sorter_jump.scara)<br>[`19_high_speed_sorter_jump.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/19_high_speed_sorter_jump.bin) |
| **20** | Annular Inspection Scan | Coordinated multi-point annular circular scan routine | [`20_annular_inspection_scan.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/20_annular_inspection_scan.scara)<br>[`20_annular_inspection_scan.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/20_annular_inspection_scan.bin) |
| **21** | Incremental Relative Motion | Incremental relative Cartesian tool moves with active work frame mapping (`MOVE_REL`) | [`21_relative_motion_incremental.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/21_relative_motion_incremental.scara)<br>[`21_relative_motion_incremental.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/21_relative_motion_incremental.bin) |
| **22** | Conveyor Tracking Relative | High-speed conveyor synchronized incremental pick-and-place tracking (`MOVE_REL`) | [`22_conveyor_tracking_relative.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/22_conveyor_tracking_relative.scara)<br>[`22_conveyor_tracking_relative.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/22_conveyor_tracking_relative.bin) |
| **23** | Bidirectional Arc Contour | High-speed smooth bidirectional arc transition with dynamic feedrates (`ARC_CW`, `ARC_CCW`) | [`23_bidirectional_arc_contour.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/23_bidirectional_arc_contour.scara)<br>[`23_bidirectional_arc_contour.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/23_bidirectional_arc_contour.bin) |
| **24** | Matrix Pallet Depalletizing | Automated depalletizing grid extraction with coordinate frame mapping | [`24_matrix_pallet_depalletizing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/24_matrix_pallet_depalletizing.scara)<br>[`24_matrix_pallet_depalletizing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/24_matrix_pallet_depalletizing.bin) |
| **25** | Stepper Motor Calibration | Closed-loop stepper encoder calibration and torque testing (`CONFIG MOTOR`) | [`25_stepper_motor_calibration.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/25_stepper_motor_calibration.scara)<br>[`25_stepper_motor_calibration.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/25_stepper_motor_calibration.bin) |
| **26** | Multi-Zone High Speed Blending | Continuous high-velocity trajectory with mixed fine and coarse zone blending (`ZONE`) | [`26_multi_zone_high_speed_blending.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/26_multi_zone_high_speed_blending.scara)<br>[`26_multi_zone_high_speed_blending.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/26_multi_zone_high_speed_blending.bin) |
| **27** | Emergency Hold Recovery | In-flight trajectory pause, sensor verification, and motion resumption (`HOLD`, `RESUME`) | [`27_emergency_hold_recovery.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/27_emergency_hold_recovery.scara)<br>[`27_emergency_hold_recovery.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/27_emergency_hold_recovery.bin) |
| **28** | Three-Frame Assembly Station | Multi-station fixture transformations across base, feeder, and nest (`FRAME_SET`, `FRAME_RESET`) | [`28_three_frame_assembly_station.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/28_three_frame_assembly_station.scara)<br>[`28_three_frame_assembly_station.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/28_three_frame_assembly_station.bin) |
| **29** | Precision Dispensing Tangent | Constant-velocity continuous adhesive contouring with tangential tool yaw (`TOOL_ORIENT TANGENT`) | [`29_precision_dispensing_tangent.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/29_precision_dispensing_tangent.scara)<br>[`29_precision_dispensing_tangent.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/29_precision_dispensing_tangent.bin) |
| **30** | Complex Automation Workcell | Fully integrated assembly cell combining pallets, frames, blending, and pneumatics | [`30_complex_automation_workcell.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/30_complex_automation_workcell.scara)<br>[`30_complex_automation_workcell.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/30_complex_automation_workcell.bin) |
| **31** | Subroutine Pick Place | Parametric pick-and-place routines using modular subroutines (`DEF`, `CALL`, `END`) | [`31_subroutine_pick_place.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/31_subroutine_pick_place.scara)<br>[`31_subroutine_pick_place.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/31_subroutine_pick_place.bin) |
| **32** | Repeat Loop Array | Automated repetitive grid testing using fixed-count iteration loops (`REPEAT`, `END`) | [`32_repeat_loop_array.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/32_repeat_loop_array.scara)<br>[`32_repeat_loop_array.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/32_repeat_loop_array.bin) |
| **33** | Nested Repeat Palletizing | Multi-layer nested iteration loops with relative coordinate indexing | [`33_nested_repeat_palletizing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/33_nested_repeat_palletizing.scara)<br>[`33_nested_repeat_palletizing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/33_nested_repeat_palletizing.bin) |
| **34** | Subroutine Relative Motion | Subroutine routines integrating relative Cartesian moves and frame offsets | [`34_subroutine_with_relative_motion.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/34_subroutine_with_relative_motion.scara)<br>[`34_subroutine_with_relative_motion.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/34_subroutine_with_relative_motion.bin) |
| **35** | Complex Cycle Subroutines Loops | Full industrial automation routine combining nested loops, subroutines, and error recovery | [`35_complex_cycle_subroutines_and_loops.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/35_complex_cycle_subroutines_and_loops.scara)<br>[`35_complex_cycle_subroutines_and_loops.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/35_complex_cycle_subroutines_and_loops.bin) |
| **36** | Spatial Keep-Out Zones | User-defined rectangular box and circular obstacle keep-out zones (`ZONE_DEF BOX`, `ZONE_DEF CIRCLE`) | [`36_spatial_keepout_zones.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/36_spatial_keepout_zones.scara)<br>[`36_spatial_keepout_zones.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/36_spatial_keepout_zones.bin) |
| **37** | Multi-Obstacle Dual Elbow | Obstacle avoidance (BOX & CIRCLE) with in-flight dynamic elbow reconfiguration (`CONFIG ELBOW`) | [`37_obstacle_avoidance_dual_elbow.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/37_obstacle_avoidance_dual_elbow.scara)<br>[`37_obstacle_avoidance_dual_elbow.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/37_obstacle_avoidance_dual_elbow.bin) |
| **38** | Nested Matrix Frame Sorting | Angled work frame transformations (`FRAME_SET`), nested iteration loops (`REPEAT`), and relative moves (`MOVE_REL`) | [`38_nested_matrix_frame_sorting.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/38_nested_matrix_frame_sorting.scara)<br>[`38_nested_matrix_frame_sorting.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/38_nested_matrix_frame_sorting.bin) |
| **39** | Closed-Loop Contour Hold Recovery | Bidirectional circular arcs (`ARC_CW`/`CCW`), corner blending (`ZONE BLEND`), and in-flight feed hold/resume (`HOLD`/`RESUME`) | [`39_closed_loop_contour_hold_recovery.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/39_closed_loop_contour_hold_recovery.scara)<br>[`39_closed_loop_contour_hold_recovery.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/39_closed_loop_contour_hold_recovery.bin) |
| **40** | Pallet Obstacle Jump Transfer | Dual matrix pallets (`PALLET_DEF`), 3D parabolic jump arch (`JUMP`), and keep-out corridor navigation | [`40_pallet_obstacle_jump_transfer.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/40_pallet_obstacle_jump_transfer.scara)<br>[`40_pallet_obstacle_jump_transfer.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/40_pallet_obstacle_jump_transfer.bin) |
| **41** | Dynamic Feedrate & Accel Profiling | Multi-stage dynamic velocity and acceleration scheduling (`ACCEL`, `SPEED WORK`, `OVERRIDE`, `ZONE BLEND`) | [`41_dynamic_feedrate_accel_profiling.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/41_dynamic_feedrate_accel_profiling.scara)<br>[`41_dynamic_feedrate_accel_profiling.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/41_dynamic_feedrate_accel_profiling.bin) |
| **42** | Vacuum Decay & Pressure Equalization | High-precision vacuum seal validation, multi-stage pressure equalization micro-dwells (`WAIT_MS`, `PUMP`, `VALVE`, `APPROACH`) | [`42_vacuum_decay_pressure_equalization.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/42_vacuum_decay_pressure_equalization.scara)<br>[`42_vacuum_decay_pressure_equalization.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/42_vacuum_decay_pressure_equalization.bin) |
| **43** | Concentric Pocket Milling Tangency | Multi-depth concentric pocket profiling with alternating circular arcs, incremental Z depth stepping, and tool tangency (`ARC_CW`/`CCW`, `TOOL_ORIENT TANGENTIAL`) | [`43_tangential_pocket_milling.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/43_tangential_pocket_milling.scara)<br>[`43_tangential_pocket_milling.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/43_tangential_pocket_milling.bin) |
| **44** | Hierarchical Subroutine Chain | 3-level deep subroutine call stack expansion (Master -> Task -> Atomic) with recursion tracking (`DEF`, `CALL`, `END`) | [`44_hierarchical_subroutine_chain.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/44_hierarchical_subroutine_chain.scara)<br>[`44_hierarchical_subroutine_chain.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/44_hierarchical_subroutine_chain.bin) |
| **45** | Polar Rotary Inspection Sweep | Polar quadrant arc sweeps with discrete 4th-axis yaw re-orientation and camera exposure dwell (`ARC_CCW`, `MOVE_REL PHI`, `WAIT_MS`) | [`45_polar_rotary_inspection_sweep.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/45_polar_rotary_inspection_sweep.scara)<br>[`45_polar_rotary_inspection_sweep.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/45_polar_rotary_inspection_sweep.bin) |
| **46** | Rotated Frame Relative Stepping | Angled work frame transformations (`FRAME_SET ... ANGLE=30.0`), relative incremental raster steps (`MOVE_REL`), and base reset (`FRAME_RESET`) | [`46_rotated_frame_relative_stepping.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/46_rotated_frame_relative_stepping.scara)<br>[`46_rotated_frame_relative_stepping.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/46_rotated_frame_relative_stepping.bin) |
| **47** | Asymmetric Dual Obstacle Channel | Tight collision-free corridor navigation between rectangular enclosure (`ZONE_DEF BOX`) and cylindrical column (`ZONE_DEF CIRCLE`) with blend transitions | [`47_asymmetric_dual_obstacle_channel.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/47_asymmetric_dual_obstacle_channel.scara)<br>[`47_asymmetric_dual_obstacle_channel.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/47_asymmetric_dual_obstacle_channel.bin) |
| **48** | Hybrid Motor Mode Torque Switch | Dynamic runtime switching between open-loop high-speed transit and closed-loop delicate seating (`CONFIG MOTOR OPEN_LOOP`/`CLOSED_LOOP`) | [`48_hybrid_motor_mode_torque_switch.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/48_hybrid_motor_mode_torque_switch.scara)<br>[`48_hybrid_motor_mode_torque_switch.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/48_hybrid_motor_mode_torque_switch.bin) |
| **49** | Serpentine Raster Dispensing | Continuous planar serpentine meander path with linear passes joined by 180° alternating circular U-turn arcs (`ARC_CW`/`CCW`, `TOOL_ORIENT TANGENTIAL`, `ZONE BLEND`) | [`49_serpentine_raster_dispensing.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/49_serpentine_raster_dispensing.scara)<br>[`49_serpentine_raster_dispensing.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/49_serpentine_raster_dispensing.bin) |
| **50** | Master Multi-System Production Cell | Full-scale capstone manufacturing cell integrating pallets, frames, obstacle keep-out, parabolic jumps, subroutines, tool tangency, and pneumatics | [`50_master_multisystem_production_cell.scara`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/50_master_multisystem_production_cell.scara)<br>[`50_master_multisystem_production_cell.bin`](file:///data/dev/python/3_tools/scaralang/github/scaralang/examples/50_master_multisystem_production_cell.bin) |

---

### 5.3 Toolchain CLI Workflows (Compile, Disassemble, Decompile)

Developers and integrators can use the `scaralang` command-line interface to compile, inspect, disassemble, decompile, and export any example program:

#### 1. Compilation (`compile`)
Compiles a human-readable `.scara` script into a packed binary execution stream (`.bin`):
```bash
scaralang compile -s examples/12_industrial_pick_place.scara -o examples/12_industrial_pick_place.bin
```

#### 2. Disassembly (`disassemble`)
Decodes binary wire protocol frames into formatted textual inspection instructions (`.dis`):
```bash
scaralang disassemble -b examples/12_industrial_pick_place.bin -o examples/12_industrial_pick_place.dis
```

#### 3. Decompilation (`decompile`)
Reconstructs high-level `.scara` DSL instructions directly from binary wire frames (`_decompiled.scara`):
```bash
scaralang decompile -b examples/12_industrial_pick_place.bin -o examples/12_industrial_pick_place_decompiled.scara
```

#### 4. Trajectory Export (`export`)
Exports trajectory plans to multi-target formats (G-code, CSV time series, JSON telemetry, SVG visualization):
```bash
scaralang export -s examples/12_industrial_pick_place.scara -f gcode -o examples/12_pick_place.gcode
scaralang export -s examples/12_industrial_pick_place.scara -f svg -o examples/12_pick_place.svg
scaralang export -s examples/12_industrial_pick_place.scara -f csv -o examples/12_pick_place.csv
scaralang export -s examples/12_industrial_pick_place.scara -f json -o examples/12_pick_place.json
```

#### 5. Static Linter Analysis (`lint`)
Validates robotic motion safety, pneumatic timing, and kinematic boundaries before execution:
```bash
scaralang lint -s examples/12_industrial_pick_place.scara
```

---

## 6. Complete Industrial Example Scripts

### 6.1 High-Speed Pick and Place with Matrix Pallet

```scara
# ------------------------------------------------------------------
# Industrial Palletizing Routine: Pick from Feeder, Place into Tray
# ------------------------------------------------------------------
CONFIG ELBOW LEFT
CONFIG MOTOR CLOSED_LOOP

SPEED RAPID 220.0
SPEED WORK 80.0
ACCEL 600.0
OVERRIDE 100

# 1. Calibrate reference home
HOME

# 2. Define a 3x4 Component Tray Matrix
PALLET_DEF TRAY_OUT ROWS 3 COLS 4 DX 30.0 DY 30.0 Z 10.0

# 3. Position above component feeder station
MOVE_J X 120.0 Y -60.0 Z 40.0
APPROACH DIST 35.0

# 4. Grip first component
PUMP ON
WAIT 150
RETRACT DIST 35.0

# 5. High-speed parabolic arch transfer to Pallet Slot #1
JUMP X 180.0 Y 50.0 Z 10.0 ARCH 30.0

# 6. Release component
PUMP OFF
VALVE ON
WAIT 60
VALVE OFF

# 7. Move directly to Pallet Slot #2 for second cycle
MOVE_PALLET TRAY_OUT INDEX 2
APPROACH DIST 10.0
```

---

### 6.2 Circular Profiling with Tool Tangency

```scara
# ------------------------------------------------------------------
# Continuous Circular Gasket Dispensing with Tangential Tool Yaw
# ------------------------------------------------------------------
SPEED RAPID 180.0
SPEED WORK 50.0
ACCEL 400.0

HOME
ZONE Z5
TOOL_ORIENT TANGENT

# Approach starting contour point
MOVE_J X 150.0 Y 0.0 Z 25.0
MOVE_L X 150.0 Y 0.0 Z 5.0

# Dispenser ON
TOOL DOWN
WAIT 50

# Continuous circular toolpath (R=40mm)
ARC_CW X 190.0 Y 40.0 I 0.0 J 40.0
ARC_CW X 230.0 Y 0.0 I 0.0 J -40.0
ARC_CW X 190.0 Y -40.0 I -40.0 J 0.0
ARC_CW X 150.0 Y 0.0 I 0.0 J 40.0

# Dispenser OFF
ZONE EXACT
TOOL UP
RETRACT DIST 30.0
```

---

### 6.3 Surface Probing and Adhesive Dispensing

```scara
# ------------------------------------------------------------------
# PCB Height Surface Probing and Touch-Off
# ------------------------------------------------------------------
CONFIG ELBOW RIGHT
SPEED RAPID 150.0
SPEED WORK 30.0

HOME

# Move above PCB test pad
MOVE_J X 140.0 Y 20.0 Z 35.0

# Search for PCB top plane at controlled velocity
PROBE SPEED 5.0 DIST 30.0

# Set Work Coordinate System relative to probed surface
FRAME X 140.0 Y 20.0 Z 0.0

# Dispense micro-dot exactly 0.5 mm above probed surface
MOVE_L X 0.0 Y 0.0 Z 0.5
TOOL DOWN
WAIT 100
TOOL UP
RETRACT DIST 20.0
FRAME_RESET
```
