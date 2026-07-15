# Agent Instructions: Python (`uv`) Mac Project

This file defines the environment, constraints, and operational guidelines for AI agents working on this repository. Adhere to these rules strictly.

---

## Environment & Run Commands

* **Operating System:** macOS
* **Python Executable:** Always invoke Python using `python3`. Do not use `python` or `pip` directly.
* **Testing:** Run tests via the `pytest` module through Python.
  * *Example:* `python3 -m pytest tests/`

## Dependency Management (`uv`)

This project uses **`uv`** for package and environment management. 
> [!CRITICAL]
> **Strict Dependency Guardrail:** Do NOT install, add, or update any third-party packages or dependencies without explicit, prior approval from the user. 

If a task requires a new package:
1. Stop and ask the user for permission.
2. Once approved, use `uv add <package>` to update the environment.

---

## Operational Guidelines

### 1. Code Style & Quality
* Write clean, idiomatic Python 3 code.
* Prefer standard library solutions over adding new dependencies whenever possible.
* Ensure all new features include corresponding unit tests in the `tests/` directory.

### 2. Execution Protocol
* Before declaring a task complete, run the test suite using `python3 -m pytest` to ensure no regressions were introduced.
* If a command fails due to a missing dependency, do not attempt to auto-install it. Report the missing dependency to the user.