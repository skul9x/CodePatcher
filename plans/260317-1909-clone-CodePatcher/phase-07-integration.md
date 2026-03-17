# Phase 07: Integration & API Bindings

Status: ⬜ Pending

---

## Objective

Kết nối Go Backend với Frontend UI thông qua các hàm Bindings của Wails. Đảm bảo luồng dữ liệu thông suốt.

---

## Requirements

- [ ] Đăng ký các Go Services (Patcher, Git, Backup) vào Wails App context.
- [ ] Implement hàm gọi từ Frontend -> Backend (e.g. `ParseText`, `ApplyPatch`, `GetHistory`, `DoGitPush`).
- [ ] Thêm tính năng Debounce khi gõ Text sẽ gọi hàm `ParseText` gửi về danh sách files TreeView.
- [ ] Kết nối tính năng Toast Notification lên màn hình mỗi khi xử lý xong I/O.

---

## Tasks

- [ ] Chỉnh sửa `main.go` / `app.go` export toàn bộ methods quan trọng.
- [ ] Chạy lệnh `wails dev` (hoặc build bindings) để Wails tự sinh file TS/JS.
- [ ] Update Frontend components gọi tới `window.go.my.app.Service.Method...` thay vì mock data.
- [ ] Xử lý error handler ở Frontend (hiển thị Dialog Error nếu file syntax lỗi hoặc backup xịt).

---

## Files

- `app.go`
- `frontend/wailsjs/` (Tự sinh)
- Các file React component tương ứng cập nhật logic gọi API.

---

## Test Criteria

- Toàn bộ flow: User chọn thư mục -> Dán mã -> Ứng dụng preview đúng -> Bấm Apply -> Khôi phục đúng cấu trúc thư mục -> Apply thành công -> Bấm qua Git Push -> Pushed lên remote -> (Bấm Rollback -> quay về cũ). Hoạt động hoàn hảo 100%.
