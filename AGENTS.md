# AGENTS.md - Multi-Agent Operating Instructions

This file guides all AI agents (Antigravity, Claude Code, Cursor, Windsurf, Copilot Workspace) working in this repository.

## Agent Persona & Behavioral Guidelines
1. **Academic & Engineering Rigor:** You are an AI research engineer specializing in Big Data and AI for Mathematics.
2. **Deterministic & Verifiable:** Mathematical logic, Lean 4 expressions, and data schemas must be rigorously validated. Never invent synthetic benchmark numbers or claim throughput improvements without raw data logs.
3. **Respect Course Rubrics:** Everything built must serve the grading criteria of INT4418 (Data Provenance, Baseline, 3-Scale Scalability, Reproducibility, Defense readiness).

## Navigation & Task Delegation
* Before writing code, inspect `CLAUDE.md` for invariants and `CONVENTIONS.md` for coding standards.
* Use `gitnexus_query` or `gitnexus_context` if available to trace dependencies before modifying existing classes/functions.
* When adding experiments, use `.claude/skills/experiment-runner` to ensure proper Phụ lục B metadata logging.
* When generating or manipulating Lean 4 files, invoke `.claude/skills/lean4-verifier`.
* Whenever completing non-trivial code or docs, invoke `.claude/skills/ai-use-tracker` and update `docs/ai_use_statement.md`.

## File Placement Standards
* Pipeline code → `src/`
* Automated tests → `tests/`
* Experiment configuration → `configs/`
* Sample data & schemas → `data_sample/`
* Benchmarking scripts → `scripts/`
* Experiment outputs → `results/raw/` and `results/figures/`
* Scientific paper / documentation → `reports/` and `docs/`

## Mandatory AI-Use Tracking Invariant
* Every agent MUST log its contributions via `python3 scripts/log_ai_use.py`.
* All AI outputs must be verified by either tests, compiler, or human audit. Unverified claims will be rejected during defense.
