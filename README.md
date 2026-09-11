# PTIT INT4418 - Dữ liệu lớn (Big Data)
## Đề tài: Hệ thống Dữ liệu lớn phục vụ Toán học & Suy luận hình thức (AI4Math)

Học phần: **INT4418 - Dữ liệu lớn (Trình độ Thạc sĩ)**  
Giảng viên hướng dẫn: **TS. Nguyễn Kiều Linh**  
Đơn vị: Khoa Trí tuệ Nhân tạo - Học viện Công nghệ Bưu chính Viễn thông (PTIT)

---

## 1. Tổng quan & Thành viên nhóm

* **Đề tài:** **NHÓM 6 — Verifier-Guided Repair** (Sửa bản Lean dựa trên phản hồi kiểm chứng).
* **Mục tiêu:** Giải quyết các nút thắt kỹ thuật về lập lịch hàng đợi phân tán, điều phối đa worker kiểm chứng Lean 4, kiểm soát độ trễ đuôi ($P95$) và bùng nổ chi phí token khi sửa lỗi tự động cho hàng nghìn mã toán hình thức.

### Danh sách thành viên Nhóm 6:
| STT | Mã học viên | Họ và tên | Vai trò phụ trách chính | Vai trò dự phòng |
|:---:|:---:|:---|:---|:---|
| 1 | **B25CHHT112** | **Đào Văn Tâm** *(Trưởng nhóm)* | Evaluation & Cost Analysis (Lead) | Queue & Worker System |
| 2 | **B25CHHT117** | **Lâm Thành Trung** | Queue & Worker System Lead | Evaluation & Cost Analysis |
| 3 | **B25CHHT119** | **Nguyễn Xuân Tùng** | LLM Repair Engine Lead | Rule-based Repair |
| 4 | **B25CHHT088** | **Trần Quang Đức Dũng** | Rule-based Repair Lead | LLM Repair Engine |
| 5 | **B25CHHT125** | **Khamsing OUTHAIHUENG** | Parser & Taxonomy Lead | Error Dataset & Contract |
| 6 | **B25CHHT124** | **Mekdala Nounou** | Error Dataset & Contract Lead | Parser & Taxonomy |

---

## 2. Cấu trúc thư mục dự án

```text
.
├── .claude/                  # AI & Claude Code harness, skills và agent configurations
│   └── skills/               # Reusable skills (experiment-runner, lean4-verifier, ...)
├── .gitnexus/                # GitNexus code intelligence index & MCP configurations
├── configs/                  # File cấu hình tham số thí nghiệm (YAML/JSON)
├── data_sample/              # Dữ liệu mẫu hợp pháp (< 5MB) và manifest checksums
├── docs/                     # Tài liệu thiết kế, data cards, AI-use statement
│   ├── references/           # Giáo trình tham khảo (Lin & Dyer, MMDS, Han & Kamber)
│   └── syllabus/             # Đề cương học phần và hướng dẫn bài tập lớn
├── reports/                  # Báo cáo học phần 12-20 trang (PDF/Docx)
├── results/
│   ├── figures/              # Biểu đồ đánh giá tạo tự động bằng script
│   └── raw/                  # Dữ liệu thực nghiệm thô theo chuẩn Phụ lục B (JSONL)
├── scripts/                  # Script tải dữ liệu lớn, chạy benchmark, vẽ đồ thị
├── slides/                   # Slide bài giảng và kịch bản demo bảo vệ
├── src/                      # Mã nguồn chính của pipeline
├── tests/                    # Kiểm thử tự động (Unit test, Integration test)
├── AGENTS.md                 # Chỉ dẫn thống nhất cho các tác tử AI
├── CLAUDE.md                 # AI harness, lệnh thực thi và ràng buộc kỹ thuật
├── CONVENTIONS.md            # Tiêu chuẩn code, commit Git và logging thực nghiệm
├── contributions.md          # Phân công vai trò 6-7 thành viên và nhật ký đóng góp
├── requirements.txt          # Danh sách thư viện Python phụ thuộc
└── README.md                 # Tài liệu hướng dẫn tổng quan dự án
```

---

## 3. Hướng dẫn cài đặt & Chạy nhanh (Quick Start)

### 3.1. Khởi tạo môi trường
```bash
# 1. Tạo môi trường ảo Python 3.10+
python3 -m venv .venv
source .venv/bin/activate

# 2. Cài đặt các gói phụ thuộc
pip install -r requirements.txt
```

### 3.2. Chạy kiểm thử tự động
```bash
pytest tests/ -v
```

### 3.3. Chạy Baseline thử nghiệm
```bash
python3 -m src.baseline --config configs/baseline.yaml
```
Kết quả thực nghiệm sẽ được ghi tự động vào `results/raw/run_<run_id>.json`.

---

## 4. Quy tắc thực nghiệm & Tái lập (Reproducibility)

Theo quy định học phần, mọi báo cáo kết quả phải tuân thủ:
1. **Có Baseline so sánh:** Luôn chạy phương pháp cơ sở trước trên cùng tập split dữ liệu và cùng phần cứng.
2. **Benchmark 3 mức quy mô:** Đo lường trên 3 mức dữ liệu / tải (Tier 1 $ightarrow$ Tier 2 $ightarrow$ Tier 3).
3. **Chỉ số bắt buộc:** Bắt buộc ghi nhận độ trễ phân vị $P50$ và $P95$, không dùng giá trị trung bình đơn lẻ.
4. **Không commit dữ liệu lớn vào Git:** Chỉ lưu mẫu nhỏ trong `data_sample/`. Dữ liệu lớn được tải qua script.

---

## 5. Tác tử AI & Tích hợp GitNexus

Dự án đã được trang bị đầy đủ bộ **AI Harness** để phối hợp với các trợ lý AI (Claude Code, Cursor, Antigravity):
* **Harness & Conventions:** Quy định chặt chẽ trong `CLAUDE.md` và `CONVENTIONS.md`.
* **GitNexus:** Quản lý biểu đồ quan hệ mã nguồn (Knowledge Graph) phục vụ phân tích phụ thuộc và blast radius.
* **Skills:** Bộ kỹ năng tự động hóa trong `.claude/skills/`.
