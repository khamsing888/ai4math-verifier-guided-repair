-- ====================================================================
-- Ví dụ mã Lean 4 có lỗi (SYNTAX_ERROR - Thiếu keyword "by")
-- Phục vụ kiểm thử trực quan trên VS Code Infoview & Error Parser
-- ====================================================================

theorem error_syntax_demo (n : Nat) : n + 0 = n :=
  -- Lỗi cú pháp: Trong Lean 4, để gọi tactic "rfl" cần có từ khóa "by"
  rfl
