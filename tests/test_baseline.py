"""Unit tests for baseline execution and metrics calculation."""

import os
import pytest
from src.baseline import run_baseline


def test_run_baseline(tmp_path):
    record = run_baseline("configs/baseline.yaml")
    assert "run_id" in record
    assert record["status"] == "SUCCESS"
    assert "latency_p50_ms" in record["metrics"]
    assert "latency_p95_ms" in record["metrics"]
    assert record["metrics"]["latency_p95_ms"] >= record["metrics"]["latency_p50_ms"]
