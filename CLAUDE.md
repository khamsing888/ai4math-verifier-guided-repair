# CLAUDE.md - AI Harness & Engineering Guide

## 1. Project Context
* **Course:** INT4418 - Dữ liệu lớn (Big Data) - Master of Science in CS / AI, PTIT (2026).
* **Instructor:** TS. Nguyễn Kiều Linh (Faculty of AI, Posts and Telecommunications Institute of Technology).
* **Domain:** AI4Math Systems & Large-Scale Data Engineering (Lean 4, LeanDojo, mathlib4, ProofNet, NuminaMath).
* **Target:** Production-grade reproducible engineering pipeline, baseline comparison, 3-scale latency/throughput evaluations, Master-level scientific report.

---

## 2. Directory Layout
* `src/`: Core modular pipeline code (ingestion, processing, retrieval, indexing, serving).
* `tests/`: Automated unit and integration tests (`pytest`).
* `configs/`: Structured experiment and pipeline configuration files (YAML/JSON).
* `data_sample/`: Legal, lightweight sample datasets, schema manifests, and checksums.
* `scripts/`: Automated data fetchers, benchmark harnesses, and plot generation scripts.
* `results/raw/`: Immutable raw experiment outputs (JSONL/CSV) keyed by `run_id`.
* `results/figures/`: Publication-quality figures and tables generated strictly from raw results.
* `docs/`: Data cards, system cards, AI-use statements, and syllabus documents.
* `docs/syllabus/`: Official course syllabus and assignment guidelines.
* `docs/references/`: Academic textbooks and foundation literature.
* `slides/`: Presentation slides and demonstration scenarios.
* `reports/`: Master course project report (12-20 pages, PDF/LaTeX/Word).
* `contributions.md`: Team role division, pull requests, issue trackers, individual defense logs.

---

## 3. Essential Commands

### Environment & Dependencies
```bash
# Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing & Code Quality
```bash
# Run all tests
pytest tests/ -v

# Run linting and formatting
ruff check src/ tests/ scripts/
ruff format src/ tests/ scripts/

# Type checking
mypy src/
```

### Experiment Execution & Benchmarking
```bash
# Run standard baseline
python3 -m src.baseline --config configs/baseline.yaml

# Run scalability experiment across 3 tiers (small, medium, large)
python3 scripts/run_experiment.py --config configs/exp_scale.yaml --scale tier1
python3 scripts/run_experiment.py --config configs/exp_scale.yaml --scale tier2
python3 scripts/run_experiment.py --config configs/exp_scale.yaml --scale tier3

# Generate paper figures from raw results
python3 scripts/generate_figures.py --input results/raw/ --output results/figures/
```

---

## 4. Engineering & Academic Invariants (STRICT RULES)

### Rule 1: Baseline-First Requirement
* Never propose or implement complex models (e.g., Deep Learning, HNSW, Graph neural networks) before a trivial, reproducible baseline is established (e.g., exact search, rule-based, TF-IDF/BM25).
* Baselines must use the exact same data split, evaluation protocol, hardware budget, and seeds.

### Rule 2: 3-Tier Scalability Benchmarks
* All Big Data claims must be demonstrated across at least **3 scale tiers** (e.g., 10K → 100K → Full, or 100 → 1K → 10K concurrency).
* Always report both **Quality** (Recall@k, MRR, compile rate) and **Cost/Resource** (P50/P95 latency, QPS, peak RAM/VRAM, disk footprint).
* Never report average latency alone; **P95 latency** is mandatory.

### Rule 3: Experiment Provenance & Logging
* Every experiment run must record an immutable record in `results/raw/run_<run_id>.json` containing:
  `run_id`, `timestamp`, `git_commit`, `data_version`, `machine` (CPU/RAM/GPU/OS), `software` versions, `parameters`, `seed`, `timeout`, `metrics`, and `status`.

### Rule 4: Zero Heavy Data in Git
* Never commit datasets or weights > 50MB to Git.
* Store small samples (< 5MB) in `data_sample/`. Large datasets must be loaded via deterministic scripts with checksum validation (`scripts/download_data.sh`).

### Rule 5: Continuous AI-Use Statement & Quantitative Logging (MANDATORY)
* In accordance with PTIT INT4418 Master course rubrics, every substantial AI intervention (code generation, refactoring, taxonomy design, benchmark scripts, documentation) MUST be logged in `docs/ai_use_log.jsonl` and reflected in `docs/ai_use_statement.md`.
* Use the automated utility:
  ```bash
  python3 scripts/log_ai_use.py --stage "<Stage>" --type "<TaskType>" --desc "<Description>" --verify "<VerificationMethod>" --lines <ApproxLines>
  ```
* All generated Lean 4 mathematical expressions, tactics, and code must be deterministically verified (by Lean 4 compiler or unit tests); raw AI claims are strictly prohibited.
* The quantitative summary in `docs/ai_use_statement.md` will be directly incorporated into Section 8 & Appendix of the final report.

---

<!-- gitnexus:start -->
## 5. GitNexus Code Intelligence Integration
GitNexus indexes this codebase into an AST knowledge graph to support deep semantic queries and blast radius analysis.
* **CLI Analysis:** `npx gitnexus analyze` to update graph index.
* **Status:** Check index health in `.gitnexus/gitnexus.json`.
* **MCP Capabilities Available to Agents:**
  - `gitnexus_query`: Search classes, functions, contracts, and call hierarchies.
  - `gitnexus_context`: Retrieve 360-degree symbol dependencies and caller-callee chains.
  - `gitnexus_impact`: Compute blast radius before refactoring critical modules.
<!-- gitnexus:end -->
