# Phase 01: Setup (Wails project init)

Status: ⬜ Pending

---

## Objective

Khởi tạo dự án Wails v2 với cấu trúc thư mục chuẩn và các module cơ bản. Chọn React/Vite làm frontend stack.

---

## Requirements

- [ ] Cài đặt sẵn Go và thư viện Wails CLI.
- [ ] Khởi tạo dự án dùng template `react-ts` (Frontend là React + TypeScript).
- [ ] Tổ chức lại thư mục backend Go sao cho gọn gàng (tách `services`, `models`, `utils`).
- [ ] Chạy thử ứng dụng cơ bản (`wails dev`) để xác nhận mọi thứ hoạt động.

---

## Tasks

- [ ] Chạy `wails init -n CodePatcher -t react-ts` (tại `/home/skul9x/Desktop/Test_code/CodePatcher-Go/`).
- [ ] Cấu hình `wails.json` (tên app, kích thước cửa sổ mặc định 1280x850).
- [ ] Xoá code demo thừa trong frontend (`App.tsx`, `App.css`).
- [ ] Chạy Git init cho repo mới.

---

## Files

- `wails.json`
- `frontend/src/App.tsx`
- `main.go`

---

## Test Criteria

- Cửa sổ Wails app trắng hiển thị lên thành công, không có lỗi console.
