# CONVENTIONS.md - Project Engineering Conventions

## 1. Git & Version Control

### Commit Message Format (Conventional Commits)
Format: `<type>(<scope>): <subject>`

* `feat`: A new feature or major module (e.g., `feat(retrieval): implement BM25 field-aware search`).
* `fix`: A bug fix (e.g., `fix(parser): resolve Lean 4 AST parenthesis mismatch`).
* `docs`: Documentation updates, data cards, syllabus notes (e.g., `docs(datacard): add NuminaMath provenance`).
* `perf`: Performance improvements, memory optimizations (e.g., `perf(ann): tune HNSW efSearch for latency`).
* `exp`: Experiment execution or benchmark run (e.g., `exp(scale): run 10k theorem benchmark on tier2`).
* `test`: Adding or updating tests (e.g., `test(etl): add schema validation unit tests`).
* `refactor`: Code refactoring without changing external behavior.
* `chore`: Maintenance, dependencies, gitignore updates.

### Branch Strategy
* `main`: Stable, clean, verified codebase ready for grading and defense.
* `feat/<name>`: Development of new components.
* `exp/<topic>`: Isolated branches for large-scale experiment runs.

---

## 2. Python & Code Quality Standards

* **Python Version:** 3.10+
* **Style Guide:** PEP 8 compliance enforced by `ruff`.
* **Line Length:** 100 characters max.
* **Type Annotations:** All public functions, methods, and classes must include static type hints.
* **Docstrings:** Google Python Style Guide for all modules and classes:
  ```python
  def retrieve_premises(query: str, top_k: int = 10) -> list[dict[str, Any]]:
      """Retrieves top-k candidate premises for a given Lean theorem statement.

      Args:
          query: Mathematical statement or theorem signature.
          top_k: Number of candidates to return.

      Returns:
          A list of dictionaries containing premise names, scores, and namespaces.

      Raises:
          ValueError: If query is empty or top_k <= 0.
      """
  ```

---

## 3. Data Contract & Schema Standards

* **Serialization:** Intermediate and curated datasets must be stored as Apache Parquet (`.parquet`) for columnar efficiency.
* **Schema Validation:** Every data ingestion step must strictly validate columns and types (using `pydantic` or `pyspark.sql.types.StructType`).
* **Partitioning Convention:** `partitionBy=["source", "data_version", "split"]`
* **Dataset Cards:** Every dataset processed must have a corresponding markdown card in `docs/` detailing:
  - Source URL and official citation.
  - License and usage restrictions.
  - Known biases, duplicate rate, and train/test leakage status.

---

## 4. Experiment Protocol (PTIT INT4418 - Phụ lục B)

Every benchmark or training run must produce an immutable JSON record in `results/raw/run_<run_id>.json`:

```json
{
  "run_id": "exp-20260911-0830-scale-tier2",
  "timestamp": "2026-09-11T08:30:00Z",
  "git_commit": "abcdef1234567890",
  "data_version": "mathlib4-v4.8.0-snapshot-1",
  "machine": {
    "cpu": "Apple M-series / Intel Xeon",
    "ram_gb": 32,
    "gpu": "None / CUDA RTX 4090",
    "os": "macOS / Ubuntu 22.04"
  },
  "software": {
    "python": "3.11.8",
    "pyspark": "3.5.1",
    "faiss": "1.8.0",
    "lean": "4.8.0"
  },
  "parameters": {
    "batch_size": 64,
    "top_k": 50,
    "index_type": "HNSW32"
  },
  "seed": 42,
  "timeout_seconds": 300,
  "metrics": {
    "throughput_qps": 142.5,
    "latency_p50_ms": 6.8,
    "latency_p95_ms": 14.2,
    "recall_at_10": 0.785,
    "peak_ram_mb": 1420
  },
  "status": "SUCCESS",
  "log_path": "logs/runs/run-20260911-0830.log"
}
```

---

## 5. Testing & Verification

* **Unit Tests (`tests/test_*.py`):** Test individual helper functions, data transforms, and metric calculations.
* **Mocking:** Do not make network calls or launch full clusters during standard `pytest`. Use mocks for external Lean compilers or remote databases.
* **Integration Tests:** Run on `data_sample/` to verify end-to-end pipeline execution within $< 30$ seconds.
