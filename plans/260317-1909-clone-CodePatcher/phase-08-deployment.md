# Phase 08: Build & Deployment

Status: ⬜ Pending

---

## Objective

Đóng gói ứng dụng thành file thực thi chạy độc lập trên Windows và Ubuntu 24.04.

---

## Requirements

- [ ] Bổ sung logo app, sửa các thông số app name, company trong `wails.json`.
- [ ] Fix các lỗi liên quan đến font chữ (nếu chọn font hiện đại).
- [ ] Build bundle gọn nhẹ (`-upx` nếu cần thiết).
- [ ] Viết hướng dẫn (README) cách chạy ứng dụng trên 2 hệ điều hành.

---

## Tasks

- [ ] Cập nhật `build/appicon.png`.
- [ ] Chạy `wails build -platform windows/amd64`
- [ ] Chạy `wails build -platform linux/amd64` (Test trên Ubuntu).
- [ ] Kiểm tra dung lượng và test crash khi mở app ở vị trí đường dẫn có dấu cách/tiếng Việt.

---

## Files

- `wails.json`
- `build/appicon.png`
- `README.md` (Phiên bản Go)

---

## Test Criteria

- Có 2 file output `CodePatcher.exe` và `CodePatcher` (linux_bin). Khởi chạy không bị lỗi màn hình trắng hay lỗi I/O. Tốc độ bật nhanh hơn bản Python.
