---
name: experiment-runner
description: Automates execution, monitoring, and reproducible logging of Big Data scalability experiments according to PTIT INT4418 Phụ lục B.
---

# Experiment Runner Skill

Use this skill when running benchmarks, testing scalability across tiers, or logging baseline comparisons.

## Mandatory Invariants
1. Never run benchmark tests without capturing system metadata (CPU, RAM, GPU, OS).
2. Must log seed and timeout for deterministic behavior.
3. Must calculate and report P50 and P95 latency distributions, not just average latency.
4. Output must be saved to `results/raw/run_<run_id>.json`.

## Standard Python Logging Utility
When building an experiment runner script, adhere to this structure:

```python
import time, json, platform, psutil, uuid
from datetime import datetime

def log_experiment_run(config_name: str, parameters: dict, metrics: dict, log_file: str):
    run_id = f"{config_name}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"
    record = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "parameters": parameters,
        "machine": {
            "platform": platform.platform(),
            "cpu": platform.processor(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2)
        },
        "metrics": metrics,
        "status": "SUCCESS"
    }
    output_path = f"results/raw/run_{run_id}.json"
    with open(output_path, "w") as f:
        json.dump(record, f, indent=2)
    return output_path
```
