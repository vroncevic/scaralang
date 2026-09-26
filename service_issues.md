# Application Service Layer Architectural Audit (`service_issues.md`)

This document tracks architectural compliance, SOLID principles, decomposition requirements, and clean boundary separation for the **Application Service** layer (`scaralang/core/service/`).

---

## 🏛️ Application Service Layer Guiding Principles (Source of Truth)

1. **Single Responsibility Principle (SRP):** Each service component (lexer, parser, linter, compiler) performs one dedicated use-case interactor task.
2. **Interface Segregation (ISP) & Structural Typing:** Consumer contracts are defined as `@runtime_checkable Protocol` interfaces without concrete inheritance (`class Foo:` rather than `class Foo(IFoo):`).
3. **No Whole Module Imports (Strictly Granular Imports Only):** Never `import os`, `import sys`, etc.
4. **Mandatory `from __future__ import annotations`:** Placed immediately after header docstring.
5. **No `__all__` and No Re-Exports in `__init__.py`:** Strictly metadata-only.

---

## 📊 Master Status Matrix

| Component / Submodule | File | Line Count | Audit Status | Violations Identified | Actionable Remediation |
|---|---|---|---|---|---|
| `core/service/dsl/` | Lexer, Parser, Linter, Compiler | ~100-200 lines | 🟢 COMPLIANT | None | Focused compiler pipeline interactors |
| `core/service/protocol/` | Protocols (IBinaryFrameBuilder, etc.) | ~50 lines each | 🟢 COMPLIANT | None | Pure structural protocols |

---

## 📋 Architectural Issues & Remediation Log

*Initial setup — zero unresolved issues.*
