# Domain Model Layer Architectural Audit (`model_issues.md`)

This document tracks architectural compliance, SOLID principles, decomposition requirements, and clean boundary separation for the **Domain Model** layer (`scaralang/core/model/`).

---

## 🏛️ Domain Model Layer Guiding Principles (Source of Truth)

1. **Pure Data Objects & Value Objects:** All models in `core/model/` must remain 100% pure data representations without business logic, network communication, hardware framing, or storage dependencies.
2. **Immutability & Safety:** Where applicable, models use frozen dataclasses or pure attribute storage.
3. **Mandatory `from __future__ import annotations`:** Every Python file must start with postponed evaluation of annotations.
4. **Dedicated Single-Class Modules:** Exactly one class or enum per file in `snake_case.py`.
5. **No `__all__` and No Re-Exports in `__init__.py`:** Package `__init__.py` files remain metadata-only.

---

## 📊 Master Status Matrix

| Component / Submodule | File | Line Count | Audit Status | Violations Identified | Actionable Remediation |
|---|---|---|---|---|---|
| `core/model/dsl/` | AST, Tokens, Diagnostics | ~40 lines each | 🟢 COMPLIANT | None | Clean domain data models |
| `core/model/protocol/` | BinaryFrame, Enums, Status | ~50 lines each | 🟢 COMPLIANT | None | Pure protocol value objects |

---

## 📋 Architectural Issues & Remediation Log

*Initial setup — zero unresolved issues.*
