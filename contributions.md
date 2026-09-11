# CONTRIBUTIONS.md - Phân công vai trò & Nhật ký đóng góp

Môn học: INT4418 - Dữ liệu lớn (Cao học PTIT)  
Đề tài: AI4Math System (Nhóm 1 - 8)

---

## 1. Cơ cấu phân vai (Dành cho nhóm 6 - 7 thành viên)

| STT | Họ và tên | Mã học viên | Vai trò chính | Vai trò dự phòng | Nhiệm vụ phụ trách chính |
|:---:|:---|:---:|:---|:---|:---|
| 1 | *[Học viên 1]* | *[Mã HV]* | **Data / Ingestion** | System | Phụ trách data schema, scraping, manifest, Parquet lake |
| 2 | *[Học viên 2]* | *[Mã HV]* | **Quality / Preprocessing**| Evaluation | Phụ trách MinHash deduplication, data cleaning, leakage audit |
| 3 | *[Học viên 3]* | *[Mã HV]* | **Baseline Lead** | Model | Xây dựng baseline đơn giản, chạy end-to-end tuần 3 |
| 4 | *[Học viên 4]* | *[Mã HV]* | **Method / Model** | Baseline | Phát triển phương pháp chính (ANN / BM25 / Autoformalization) |
| 5 | *[Học viên 5]* | *[Mã HV]* | **Serving / Scalability** | System | Benchmark 3 mức tải, đo latency P50/P95, QPS, Memory |
| 6 | *[Học viên 6]* | *[Mã HV]* | **Evaluation & Error Analysis**| Report | Thống kê số liệu, ablation study, taxonomy phân loại lỗi |
| 7 | *[Học viên 7]* | *[Mã HV]* | **Lead & Report / Packaging**| Quality | Điều phối data contract, Docker, CI/CD, báo cáo khoa học |

> **Nguyên tắc bảo vệ:** Mỗi thành viên có vai trò chính và vai trò dự phòng. Khi bảo vệ vấn đáp, từng thành viên phải hiểu rõ toàn bộ luồng pipeline và giải trình được chi tiết phần việc mình phụ trách.

---

## 2. Nhật ký công việc và Pull Requests (PR Log)

| Tuần | Nhiệm vụ | Người thực hiện | PR / Commit | Trạng thái | Minh chứng |
|:---:|:---|:---:|:---:|:---:|:---|
| W1 | Chốt đề cương 1 trang & phân vai | Cả nhóm | - | Hoàn thành | Đề cương 1 trang (docs/de_cuong_w1.md) |
| W2 | Chốt Data Contract & Schema | TV1, TV7 | - | Đang thực hiện | Schema Parquet & mock data |
| W3 | Baseline end-to-end chạy ổn định | TV3, TV4 | - | Chờ thực hiện | Baseline code & raw metrics |
| W4 | Checkpoint đường dữ liệu | TV1, TV2 | - | Chờ thực hiện | Checkpoint report |
| W5-6| Scalability & Serving pipeline | TV4, TV5 | - | Chờ thực hiện | Pipeline v0.2 + Docker |
| W7 | Thí nghiệm 3 mức tải (Scalability) | TV5, TV6 | - | Chờ thực hiện | Raw CSV/JSON + Biểu đồ P95 |
| W8 | Error analysis & Ablation | TV6 | - | Chờ thực hiện | Bảng ablation & Taxonomy lỗi |
| W9 | Đóng gói sản phẩm & Báo cáo | TV7, Cả nhóm | - | Chờ thực hiện | Report bản thảo 12-20 trang |
| W10 | Demo & Bảo vệ vấn đáp | Cả nhóm | - | Chờ thực hiện | Slide + Live Demo + Package |
