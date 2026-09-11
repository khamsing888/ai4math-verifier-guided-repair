"""Unit tests for LeanErrorParser."""

import unittest
from src.error_parser import LeanErrorParser, ErrorCategory, RepairRoute


class TestErrorParser(unittest.TestCase):
    def test_syntax_error_classification(self):
        diag = {"line": 1, "column": 10, "message": "unexpected token ':', expected ')'"}
        record = LeanErrorParser.parse_diagnostic(diag)
        self.assertEqual(record.category, ErrorCategory.SYNTAX_ERROR)
        self.assertEqual(record.route, RepairRoute.RULE_REPAIR)

    def test_missing_import_classification(self):
        diag = {"line": 1, "column": 1, "message": "unknown package 'Mathlib.Data.Real.Basic'"}
        record = LeanErrorParser.parse_diagnostic(diag)
        self.assertEqual(record.category, ErrorCategory.MISSING_IMPORT)
        self.assertEqual(record.route, RepairRoute.RULE_REPAIR)

    def test_type_mismatch_classification(self):
        diag = {"line": 2, "column": 15, "message": "type mismatch at term 3, has type Nat but expected Int"}
        record = LeanErrorParser.parse_diagnostic(diag)
        self.assertEqual(record.category, ErrorCategory.TYPE_MISMATCH)
        self.assertEqual(record.route, RepairRoute.LLM_REPAIR)

    def test_timeout_classification(self):
        diag = {"line": 5, "column": 1, "message": "maximum heartbeats exceeded (200000)"}
        record = LeanErrorParser.parse_diagnostic(diag)
        self.assertEqual(record.category, ErrorCategory.TIMEOUT_EXCEEDED)
        self.assertEqual(record.route, RepairRoute.SYSTEM_CONTROL)


if __name__ == "__main__":
    unittest.main()
