# Tóm tắt công việc đã thực hiện

## 1. Mục tiêu
Bài tập yêu cầu sửa lỗi trong dự án `ai4math-verifier-guided-repair` để repo có thể chạy được và các test unit pass. Ngoài ra, cần ghi lại hoạt động hỗ trợ AI theo quy định của môn học INT4418.

## 2. Vấn đề ban đầu
Khi chạy test trong repo, lỗi xảy ra ở module baseline:

- file liên quan: `src/baseline.py`
- nguyên nhân: module import `numpy` trực tiếp ở thời điểm load module
- môi trường hiện tại trên máy không có `numpy`, nên chương trình bị lỗi ngay khi import

Lỗi ban đầu cụ thể là:

```python
ModuleNotFoundError: No module named 'numpy'
```

## 3. Cách sửa
Tôi đã sửa logic trong `src/baseline.py` bằng cách:

- bỏ dependency trực tiếp vào `numpy`
- thay bằng cách tính toán bằng thư viện chuẩn của Python (`random`, `math`)
- giữ lại nguyên chức năng cần thiết của baseline:
  - sinh dữ liệu mô phỏng latency
  - tính percentile `P50` và `P95`
  - tính throughput
  - ghi file kết quả JSON vào `results/raw/`

Như vậy, chương trình vẫn chạy đúng mà không cần cài đặt `numpy` ngay trong môi trường hiện tại.

## 4. Kiểm chứng
Sau khi sửa, tôi đã chạy lệnh sau:

```bash
python -m unittest discover -s tests -v
```

Kết quả thực tế:

- `Ran 9 tests in 0.091s`
- `OK`

Điều này chứng minh toàn bộ test suite trong repo đã pass sau khi sửa.

## 5. Ghi nhận sử dụng AI theo quy định
Theo hướng dẫn của dự án, mọi hoạt động dùng AI cần được ghi nhật ký rõ ràng. Tôi đã cập nhật các file sau:

- `docs/ai_use_log.jsonl`
- `docs/ai_use_statement.md`

Nội dung ghi nhận bao gồm:

- giai đoạn làm việc
- công cụ / mô hình AI sử dụng
- loại công việc
- nội dung thực hiện
- phương thức kiểm chứng
- người kiểm duyệt

## 6. Git và branch
Tôi đã commit thay đổi vào branch:

- `feature/error-router`

Commit local:

```bash
4ea9161 fix(baseline): remove hard numpy dependency
```

Sau đó, branch đã được push lên fork của bạn trên GitHub:

- https://github.com/khamsing888/ai4math-verifier-guided-repair

## 7. Link tạo Pull Request
Bạn có thể mở link sau để tạo PR:

- https://github.com/khamsing888/ai4math-verifier-guided-repair/pull/new/feature/error-router

## 8. Kết luận
Bài tập đã được xử lý thành công ở mức code và test. Mục tiêu chính là sửa repo để chạy ổn định, pass unit tests và ghi nhận đúng quy trình AI-use theo yêu cầu môn học.

Nếu cần, bạn có thể dùng file này như một bản tóm tắt để nộp hoặc trình bày trong báo cáo nhóm.
