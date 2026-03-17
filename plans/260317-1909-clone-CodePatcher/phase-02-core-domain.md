# Phase 02: Core Domain (Regex, File IO)

Status: ✅ Complete

---

## Objective

Chuyển đổi logic Regex để bóc tách nội dung code (từ AI chat) và logic kiểm tra an toàn đường dẫn (Path Traversal) sang ngôn ngữ Go.

---

## Requirements

- [ ] Viết hàm Go parse đoạn text có chứa markdown code blocks.
- [ ] Viết hàm bảo mật `is_safe_path` để giới hạn đường dẫn bắt buộc phải nằm trong thư mục gốc dự án.
- [ ] Viết hàm `check_syntax` (giả lập hoặc gọi linter) nếu cần, hoặc tạm thời bỏ qua nếu quá phức tạp (Dry run).

---

## Tasks

- [ ] Tạo file `backend/utils/path_utils.go` chứa logic `is_safe_path`.
- [ ] Tạo file `backend/services/parser_service.go` chứa regex bóc tách block markdown (tương đương `PATCH_REGEX` trong Python).
- [ ] Viết Unit Test cơ bản trên Go cho regex và path validation để đảm bảo chính xác.

---

## Files

- `backend/utils/path_utils.go`
- `backend/services/parser_service.go`
- `backend/utils/path_utils_test.go`

---

## Test Criteria

- Parse text: Nhận diện thành công và lấy đúng nội dung file, đường dẫn file từ markdown.
- Path safety: Chặn thành công các đường dẫn chứa `../` hoặc nằm ngoài project dir.
