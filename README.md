# SCARA Robotics Domain-Specific Language (DSL) Toolchain & Binary Protocol Codec

[![GitHub Workflow Build](https://github.com/vroncevic/scaralang/actions/workflows/scaralang_python3_build.yml/badge.svg)](https://github.com/vroncevic/scaralang/actions)
[![Documentation Status](https://readthedocs.org/projects/scaralang/badge/?version=latest)](https://scaralang.readthedocs.io/en/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**scaralang** is a standalone, lightweight, GUI-independent Python toolchain and compiler for the **SCARA Robotics Domain-Specific Language (DSL)**, combined with the official **SCARA Wire Binary Protocol Codec**.

It serves as the **Single Source of Truth (SSoT)** across the entire SCARA software ecosystem, shared seamlessly between:
- **[scarajectory](https://github.com/vroncevic/scarajectory)** (Desktop Studio & Motion Trajectory Planner)
- **[scaraemu](https://github.com/vroncevic/scaraemu)** (SCARA Digital Twin Kinematic Simulator)
- **[scara_base](https://github.com/vroncevic/scara)** (Raspberry Pi Pico RP2040 C Firmware)

---

## 🚀 Key Features

* **High-Level SCARA DSL**: Lexer, Parser, AST, Linter, and Semantic Validator for human-readable robot motion scripts (`.scara`).
* **Deterministic Bytecode Compiler**: Direct translation of DSL programs into discrete motor joint step blocks (`JointSteps`, `Step`, `Program`).
* **Binary Wire Protocol Codec**: High-performance binary frame serialization and streaming parsing (`BinaryFrameBuilder`, `BinaryFrameParser`, `BinaryPayloadUnpacker`, CRC-16-CCITT).
* **CLI Tool (`scarac` / `scaralang`)**: Command-line interface for compiling, linting, and inspecting SCARA DSL programs in headless environments and CI/CD pipelines.
* **Zero GUI Dependencies**: Built on Clean Architecture and `ats_utilities` with zero Tkinter/Qt dependencies.

---

## 📦 Installation

```bash
pip install scaralang
```

Or from source:

```bash
git clone git@github.com:vroncevic/scaralang.git
cd scaralang
pip install -r requirements.txt
python3 setup.py install
```

---

## 🛠️ Usage

### CLI (`scarac`)

```bash
# Check syntax and lint program
scarac lint program.scara

# Compile DSL program to packed binary execution file
scarac compile program.scara -o program.bin
```

---

## 📄 License

GPL-3.0 License. Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>.
