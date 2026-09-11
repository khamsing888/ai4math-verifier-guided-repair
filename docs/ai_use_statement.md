# AI-USE STATEMENT (BẢN TUYÊN BỐ SỬ DỤNG AI)
### HỌC PHẦN: DỮ LIỆU LỚN (INT4418) - NHÓM 6: VERIFIER-GUIDED REPAIR

> **Quy định học phần:** Theo Hướng dẫn Bài tập lớn INT4418 và Đề cương chi tiết, việc sử dụng các mô hình AI/LLM phải được công khai minh bạch, có định lượng cụ thể, và toàn bộ mã nguồn cũng như kết luận đều phải được nhóm học viên kiểm chứng độc lập (thông qua Lean 4 compiler và automated tests).

---

## 1. Bảng số liệu định lượng tổng hợp (Quantitative Summary)

* **Tổng số phiên/hạng mục AI hỗ trợ:** `8`
* **Ước tính số dòng mã & tài liệu AI đồng hành:** `~1210` dòng
* **Cơ chế kiểm chứng bắt buộc:** 100% mã nguồn được xác minh qua unit test tự động và trình kiểm chứng Lean 4; không chấp nhận mã chưa kiểm chứng.

### Phân bổ theo loại tác vụ:
| Loại tác vụ | Số lần ghi nhận | Tỷ trọng (%) |
|:---|:---:|:---:|
| Workspace Setup | 1 | 12.5% |
| Governance & Harness | 1 | 12.5% |
| Academic Proposal | 1 | 12.5% |
| Taxonomy Design | 1 | 12.5% |
| Dataset Curation | 1 | 12.5% |
| Code Generation | 1 | 12.5% |
| Baseline Implementation | 1 | 12.5% |
| Testing & QA | 1 | 12.5% |

### Phân bổ theo mô hình / công cụ AI:
| Mô hình / Công cụ | Số lần ghi nhận | Tỷ trọng (%) |
|:---|:---:|:---:|
| Claude Code / Antigravity | 8 | 100.0% |

---

## 2. Nhật ký chi tiết hoạt động AI hỗ trợ (Chronological AI Activity Log)

| Thời điểm (UTC) | Giai đoạn | Mô hình / Công cụ | Loại tác vụ | Nội dung thực hiện | Phương thức kiểm chứng | Người kiểm duyệt | Trạng thái |
|:---|:---|:---|:---|:---|:---|:---:|:---:|
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Workspace Setup | Cấu trúc lại thư mục theo chuẩn đề cương PTIT (configs, data_sample, docs, reports, results, scripts, slides, src, tests) và phân loại tệp tin. | Kiểm tra cấu trúc cây thư mục và Git status sạch sẽ | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Governance & Harness | Thiết lập hệ thống AI harness (CLAUDE.md, AGENTS.md, CONVENTIONS.md, GitNexus knowledge graph manifest). | Review nội dung quy tắc Big Data và kiểm tra cấu hình GitNexus | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Academic Proposal | Soạn thảo Đề cương 1 trang Tuần 1 cho Nhóm 6 (Verifier-Guided Repair) theo đúng 10 mục chuẩn Phụ lục A. | Đối chiếu với rubric chấm điểm và câu hỏi nghiên cứu RQ1, RQ2 | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Taxonomy Design | Xây dựng bảng phân loại lỗi Lean 4 (Taxonomy v0.1) gồm 6 nhóm lỗi cốt lõi, cơ chế định tuyến Router và tiêu chí an toàn ngữ nghĩa. | Kiểm tra dấu hiệu nhận biết trong compiler diagnostics của Lean 4 | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Dataset Curation | Tạo tập 50 mẫu lỗi Lean 4 thực tế (error_dataset_50.json) chia 34 train (68%) và 16 hold-out (32%) chống rò rỉ dữ liệu. | Kiểm tra schema JSON và tỷ lệ phân chia train/holdout | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Code Generation | Cài đặt bộ bóc tách lỗi Lean 4 (src/error_parser.py) phân tích log và định tuyến chiến lược sửa (Rule / LLM / System / Audit). | Chạy bộ kiểm thử tự động unittest (100% pass) | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Baseline Implementation | Cài đặt Blind One-Shot Retry Baseline (src/baseline_repair.py) theo đúng đặc tả mục 7 đề tài Nhóm 6, đo latency P50/P95 và chi phí token. | Chạy thực tế end-to-end trên tập 50 lỗi, sinh file log JSON Phụ lục B | Đào Văn Tâm | ✅ VERIFIED |
| 2026-09-11 01:59 | Tuần 1 | Claude Code / Antigravity | Testing & QA | Xây dựng bộ kiểm thử tự động (tests/test_error_parser.py, tests/test_baseline.py) bao phủ các hàm phân loại và baseline. | Thực thi unittest discover, 5/5 tests passed in 0.063s | Đào Văn Tâm | ✅ VERIFIED |

---

## 3. Cam kết liêm chính học thuật (Academic Integrity Affirmation)

1. Nhóm học viên chịu trách nhiệm hoàn toàn về tính chính xác, tính logic toán học và khả năng thực thi của toàn bộ mã nguồn trong dự án.
2. Các phát biểu toán học và mã sửa Lean 4 đều phải được kiểm tra qua trình biên dịch hình thức (`lean` CLI).
3. Mọi kết quả thực nghiệm, số đo độ trễ $P50 / P95$ và thông lượng đều được sinh ra từ các lần chạy thật trên hệ thống thực tế (lưu tại `results/raw/`), không sử dụng số liệu suy diễn từ AI.
