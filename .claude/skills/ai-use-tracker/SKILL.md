---
name: ai-use-tracker
description: Quantifies, logs, and maintains the AI-Use Statement (docs/ai_use_statement.md and docs/ai_use_log.jsonl) required for the PTIT INT4418 Master Report.
---

# AI Use Tracker Skill

Use this skill whenever an AI agent completes a non-trivial engineering or research task (e.g., writing new modules, designing schemas, generating baseline code, running experiments, drafting reports).

## Invariants & Requirements
1. **Mandatory Disclosure:** All AI contributions must be logged in `docs/ai_use_log.jsonl`.
2. **Deterministic Verification:** Every log entry must state the exact verification method (e.g., Lean 4 compiler check, unit test execution, human review).
3. **Quantification:** Must estimate approximate lines of code or content created.
4. **Auto-Regeneration:** After appending a log, regenerate `docs/ai_use_statement.md` by calling `python3 scripts/log_ai_use.py`.

## CLI Usage Pattern
```bash
python3 scripts/log_ai_use.py   --stage "Tuần 2: Data Contract"   --model "Claude Code / Antigravity"   --type "Schema Validation"   --desc "Implemented Parquet schema validator and cross-group contract assertions"   --verify "Ran pytest on sample parquet schema files"   --auditor "Đào Văn Tâm"   --lines 80
```
