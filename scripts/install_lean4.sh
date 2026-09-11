#!/usr/bin/env bash
# Script cài đặt Lean 4 và Elan cho dự án AI4Math (macOS / Linux)
# Học phần: INT4418 - Dữ liệu lớn (PTIT) - Nhóm 6

set -e

echo "=== [1/4] Kiểm tra công cụ quản lý phiên bản Elan ==="
if command -v elan &> /dev/null; then
    echo "✓ Elan đã được cài đặt: $(elan --version)"
else
    echo "Đang cài đặt Elan qua script chính thức..."
    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain leanprover/lean4:stable
    source "$HOME/.elan/env"
fi

echo ""
echo "=== [2/4] Kiểm tra trình biên dịch Lean 4 và Lake ==="
source "$HOME/.elan/env" || true
if command -v lean &> /dev/null; then
    echo "✓ Lean version: $(lean --version)"
    echo "✓ Lake version: $(lake --version)"
else
    echo "❌ Chưa tìm thấy Lean trong PATH. Hãy thêm dòng sau vào ~/.zshrc hoặc ~/.bashrc:"
    echo '    source "$HOME/.elan/env"'
    exit 1
fi

echo ""
echo "=== [3/4] Cấu hình toolchain mặc định cho AI4Math ==="
elan default leanprover/lean4:v4.8.0 || elan default leanprover/lean4:stable
echo "✓ Đã đặt toolchain Lean 4 thành công."

echo ""
echo "=== [4/4] Kiểm thử biên dịch một biểu thức mẫu Lean 4 ==="
TEMP_FILE=$(mktemp /tmp/test_lean.XXXXXX.lean)
cat << 'LEAN_EOF' > "$TEMP_FILE"
theorem test_add (n : Nat) : n + 0 = n := by rfl
LEAN_EOF

echo "Đang kiểm chứng mã Lean mẫu..."
if lean --json "$TEMP_FILE" &> /dev/null; then
    echo "✓ Lean 4 biên dịch và kiểm chứng hoàn hảo!"
else
    echo "⚠️ Có lỗi khi chạy thử nghiệm."
fi
rm -f "$TEMP_FILE"

echo ""
echo "🎉 Hoàn tất cài đặt Lean 4 cho Nhóm 6!"
