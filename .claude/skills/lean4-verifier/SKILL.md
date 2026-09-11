---
name: lean4-verifier
description: Validates Lean 4 mathematical syntax, formal proofs, compiler diagnostics, and error taxonomies for AI4Math pipelines.
---

# Lean 4 Verifier Skill

Use this skill to interface with Lean 4 and `lake` for formal verification, compiler error classification, and theorem validation (relevant to Groups 3, 4, 5, 6, 7).

## Common Compiler Diagnostic Taxonomies
When capturing Lean 4 compiler output, categorize errors into:
1. `SYNTAX_ERROR`: Unparseable Lean grammar, misplaced tokens, unbalanced brackets.
2. `UNKNOWN_IDENTIFIER`: Undefined premise, missing `import` or wrong `open` namespace.
3. `TYPE_MISMATCH`: Expected type does not match the actual term type.
4. `UNSOLVED_GOALS`: Proof tactic sequence incomplete (contains `sorry` or unsatisfied goal).
5. `TIMEOUT_EXCEEDED`: Lean heartbeat or deterministic timeout exceeded (`maxHeartbeats`).

## CLI Execution Pattern
```bash
# Verify a standalone Lean 4 file with resource limits
lean --memory=4096 -D maxHeartbeats=200000 MathProblem.lean
```

## Parsing JSON Compiler Messages
Lean 4 supports outputting structured JSON diagnostics:
```bash
lean --json MathProblem.lean
```
Parse the `severity`, `pos`, and `data` fields to determine whether the statement compiles cleanly or needs repair (for Nhóm 6 Verifier-Guided Repair).
