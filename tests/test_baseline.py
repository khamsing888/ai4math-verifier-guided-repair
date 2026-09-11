"""Unit tests for baseline execution and metrics calculation."""

import unittest
from src.baseline import run_baseline


class TestBaseline(unittest.TestCase):
    def test_run_baseline(self):
        record = run_baseline("configs/baseline.yaml")
        self.assertIn("run_id", record)
        self.assertEqual(record["status"], "SUCCESS")
        self.assertIn("latency_p50_ms", record["metrics"])
        self.assertIn("latency_p95_ms", record["metrics"])
        self.assertGreaterEqual(
            record["metrics"]["latency_p95_ms"],
            record["metrics"]["latency_p50_ms"]
        )


if __name__ == "__main__":
    unittest.main()
