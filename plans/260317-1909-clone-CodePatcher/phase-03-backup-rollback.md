# Phase 03: Backup/Rollback Engine

Status: ✅ Complete

---

## Objective

Xây dựng Backup Engine để sao lưu file trước khi ghi đè, tạo lịch sử (`manifest.json`) và tính năng Rollback khôi phục lại code.

---

## Requirements

- [x] Tổ chức thư mục `backups/{batch_id}` (batch_id là timestamp).
- [x] Logic sao chép file gốc vào thư mục backup.
- [x] Logic tạo file `manifest.json` ghi nhận danh sách file cập nhật và project root.
- [x] Logic Rollback: đọc manifest và copy ngược lại từ backup vào project gốc.

---

## Tasks

- [x] Tạo file `backend/services/backup_service.go`.
- [x] Define các Struct JSON cho `manifest.json`.
- [x] Viết hàm `CreateBackup(projectDir, filePaths) error`.
- [x] Viết hàm `RollbackBatch(batchID) error`.
- [x] Viết hàm `GetHistory() []HistoryItem` để frontend gọi hiển thị.

---

## Files

- `backend/services/backup_service.go`
- `backend/models/manifest.go`

---

## Test Criteria

- Thực hiện mockup ghi đè file: File cũ được copy sang `backups/`, `manifest.json` ghi đúng cấu trúc.
- Rollback: Xóa file hiện tại, lấy file trong `backups/` đắp lại 100% nguyên bản.
