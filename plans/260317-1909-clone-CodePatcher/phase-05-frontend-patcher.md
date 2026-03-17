# Phase 05: Frontend Layout & Patcher Tab

Status: ⬜ Pending

---

## Objective

Xây dựng khung giao diện chính cho ứng dụng và tab Code Patcher dùng React (TailwindCSS hoặc CSS Modules).

---

## Requirements

- [x] Layout 2 tabs (`Code Patcher`, `GitHub Sync`).
- [x] Area Header with brand and navigations.
- [x] Giao diện Code Patcher: Splitter 2 bên. 
  - Bên trái: Textarea để dán code (hỗ trợ Nút dán siêu tốc & xóa path).
  - Bên dưới: Nút Apply và TreeView xem trước file bị thay đổi (Dry Run).
  - Bên phải: Danh sách lịch sử các đợt apply patch & Nút hoán tác (Rollback).

---

## Tasks

- [x] Cài đặt UI Library (lucide-react, react-resizable-panels).
- [x] Tạo component `SplitPane` bằng PanelGroup.
- [x] Xây dựng `PatcherTab.tsx`.
- [x] Xây dựng phần History & Preview trong tab chính.
- [ ] Gọi thử các Wails bindings mock data.

---

## Files

- `frontend/src/App.tsx`
- `frontend/src/components/PatcherTab.tsx`
- `frontend/src/components/HistoryPanel.tsx`

---

## Test Criteria

- UI responsive, chia đôi panel có thể kéo thả tương đối (nếu dùng SplitPane).
- Gõ vào khung text mượt mà. Treeview hiển thị đúng cấu trúc file ảo (chấp nhận test bằng dữ liệu tĩnh).
