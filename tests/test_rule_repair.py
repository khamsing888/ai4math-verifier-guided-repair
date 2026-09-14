"""Unit tests for Rule-based Repair Engine."""

import unittest
from pathlib import Path
from src.rule_repair import (
    RuleRepairEngine,
    apply_rules,
    evaluate_dataset,
)


class TestRuleRepairEngine(unittest.TestCase):
    """Test suite for 4 heuristic repair rules and fail-over mechanism."""

    def setUp(self) -> None:
        self.engine = RuleRepairEngine()

    # --- R1: Bracket Balancer Tests ---
    def test_r1_unmatched_square_bracket(self) -> None:
        code = "def l : List Nat := [1, 2, 3"
        msg = "expected ']'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R1_bracket_balancer")
        self.assertTrue(res.repaired_code.endswith("]"))
        self.assertEqual(res.token_cost, 0)
        self.assertLess(res.latency_ms, 5.0)

    def test_r1_unclosed_parenthesis_hypothesis(self) -> None:
        code = "theorem bar (a b : Real) (h : (a + b = 2 : a = 2 - b"
        msg = "unexpected token ':', expected ')'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R1_bracket_balancer")
        self.assertIn("(h : a + b = 2) :", res.repaired_code)

    def test_r1_unexpected_closing_paren(self) -> None:
        code = "theorem thm3 (x : Nat) : (x = x)) := by rfl"
        msg = "unexpected token ')'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R1_bracket_balancer")
        self.assertNotIn("))", res.repaired_code)

    # --- R2: Keyword Inserter Tests ---
    def test_r2_missing_colon(self) -> None:
        code = "theorem foo (n : Nat) n > 0"
        msg = "expected ':'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R2_keyword_inserter")
        self.assertEqual(res.repaired_code, "theorem foo (n : Nat) : n > 0")

    def test_r2_missing_by_tactic(self) -> None:
        code = "theorem thm1 (p q : Prop) : p ∧ q → p \n exact And.left"
        msg = "expected ':=' or '|'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R2_keyword_inserter")
        self.assertIn(":= by", res.repaired_code)

    def test_r2_unexpected_semicolon(self) -> None:
        code = "theorem thm2 : 1 + 1 = 2; := by rfl"
        msg = "unexpected token ';'"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R2_keyword_inserter")
        self.assertNotIn(";", res.repaired_code)

    def test_r2_missing_command(self) -> None:
        code = "simple_math (n : Nat) : n = n := by rfl"
        msg = "expected command"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R2_keyword_inserter")
        self.assertTrue(res.repaired_code.startswith("theorem simple_math"))

    def test_r2_ascii_arrow_replacement(self) -> None:
        code = "theorem thm4 (p q : Prop) : p -> q := by intro h"
        msg = "expected '→' or ':='"
        res = self.engine.repair_candidate(code, "SYN_01", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R2_keyword_inserter")
        self.assertIn("p → q", res.repaired_code)

    # --- R3: Mathlib Import Injector Tests ---
    def test_r3_import_real(self) -> None:
        code = "theorem real_pos (x : Real) : x^2 >= 0 := sorry"
        msg = "unknown identifier 'Real'"
        res = self.engine.repair_candidate(code, "IMP_02", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R3_mathlib_import_injector")
        self.assertIn("import Mathlib.Data.Real.Basic", res.repaired_code)

    def test_r3_import_complex(self) -> None:
        code = "theorem c_im (z : Complex) : z.im = 0 := sorry"
        msg = "unknown identifier 'Complex'"
        res = self.engine.repair_candidate(code, "IMP_02", msg)
        self.assertIsNotNone(res)
        self.assertIn("import Mathlib.Data.Complex.Basic", res.repaired_code)

    def test_r3_import_matrix(self) -> None:
        code = "def M : Matrix (Fin 2) (Fin 2) Nat := sorry"
        msg = "unknown identifier 'Matrix'"
        res = self.engine.repair_candidate(code, "IMP_02", msg)
        self.assertIsNotNone(res)
        self.assertIn("import Mathlib.Data.Matrix.Basic", res.repaired_code)

    # --- R4: Identifier Resolver Tests ---
    def test_r4_list_len_to_length(self) -> None:
        code = "def len (l : List Nat) : Nat := l.len"
        msg = "unknown identifier 'len' in List"
        res = self.engine.repair_candidate(code, "ID_03", msg)
        self.assertIsNotNone(res)
        self.assertEqual(res.rule_applied, "R4_identifier_resolver")
        self.assertIn("l.length", res.repaired_code)

    def test_r4_nat_suc_to_succ(self) -> None:
        code = "def next (n : Nat) : Nat := Nat.suc n"
        msg = "unknown constant 'Nat.suc'"
        res = self.engine.repair_candidate(code, "ID_03", msg)
        self.assertIsNotNone(res)
        self.assertIn("Nat.succ n", res.repaired_code)

    def test_r4_tactic_semip_to_simp(self) -> None:
        code = "theorem sim_t (n : Nat) : n + 0 = n := by semip"
        msg = "unknown tactic 'semip'"
        res = self.engine.repair_candidate(code, "ID_03", msg)
        self.assertIsNotNone(res)
        self.assertIn("by simp", res.repaired_code)

    # --- Fail-Over & Sub-5ms Latency Tests ---
    def test_fail_over_type_mismatch(self) -> None:
        """TYP_04 cannot be fixed by rule heuristics, must fail over to LLM."""
        code = "theorem bad : Nat := 'string'"
        msg = "type mismatch at term 'string' has type String but expected Nat"
        res = self.engine.repair_candidate(code, "TYP_04", msg)
        self.assertIsNone(res)
        self.assertIsNone(apply_rules(code, "TYP_04", msg))

    def test_fail_over_timeout(self) -> None:
        """TMO_05 cannot be fixed by rules, routed to system control."""
        code = "theorem tmo : True := sorry"
        msg = "(deterministic) timeout at tactic execution"
        res = self.engine.repair_candidate(code, "TMO_05", msg)
        self.assertIsNone(res)

    def test_evaluate_sample_dataset(self) -> None:
        """Evaluates rule coverage across the 50 error sample dataset."""
        data_path = Path("data_sample/error_dataset_50.json")
        if data_path.exists():
            metrics = evaluate_dataset(str(data_path))
            self.assertEqual(metrics["total_samples"], 50)
            self.assertGreaterEqual(metrics["rule_repaired_samples"], 24)
            self.assertGreaterEqual(metrics["rule_hit_rate"], 0.45)
            self.assertLess(metrics["avg_latency_ms"], 5.0)
            self.assertGreater(metrics["tokens_saved_approx"], 10000)


if __name__ == "__main__":
    unittest.main()

