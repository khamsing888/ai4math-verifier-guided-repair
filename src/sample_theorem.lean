-- ====================================================================
-- Ví dụ mã Lean 4 hợp lệ (Biên dịch thành công)
-- Nhóm 6: Verifier-Guided Repair (INT4418)
-- ====================================================================

theorem add_zero_identity (n : Nat) : n + 0 = n := by
  rfl

theorem mul_zero_identity (n : Nat) : n * 0 = 0 := by
  simp
