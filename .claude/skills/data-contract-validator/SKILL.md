---
name: data-contract-validator
description: Validates dataset schemas, data contracts, deduplication metrics, and leakage checks across the AI4Math pipeline groups.
---

# Data Contract Validator Skill

Use this skill to ensure consistency between upstream data providers (Nhóm 1 Data Lake, Nhóm 2 Data Quality) and downstream consumers (Nhóm 3/4 Retrieval, Nhóm 5/6 Autoformalization).

## Data Contract Validation Checklist
1. **Schema Integrity:** Verify all expected columns exist with exact data types (`theorem_id`, `statement_natural`, `statement_lean`, `source`, `split`).
2. **Missing & Null Checks:** Ensure `statement_natural` and `theorem_id` have zero null values.
3. **Deduplication Check:** Verify MinHash / Exact Hash duplicate rate is within accepted thresholds (< 1%).
4. **Data Leakage Check:** Strictly assert that $	ext{Train} \cap 	ext{Test} = \emptyset$ based on normalized problem statements and formal theorem names.

## Standard Validation Script Pattern
```python
import pyarrow.parquet as pq

def validate_contract(parquet_path: str, required_cols: list[str]) -> bool:
    schema = pq.read_schema(parquet_path)
    col_names = schema.names
    for col in required_cols:
        if col not in col_names:
            raise ValueError(f"Schema violation: missing required column {col}")
    return True
```
