# Phase 04: Git Service Integration

Status: ✅ Complete

---

## Objective

Chuyển đổi các chức năng tương tác với Git từ `GitPython` sang Go (Sử dụng `os/exec` gọi Git CLI hoặc thư viện `go-git`). 

---

## Requirements

- [x] Xử lý quản lý Token (Mã hóa cơ bản tương tự `TokenCipher` của Python).
- [x] Lấy danh sách Branches, Chuyển Branch.
- [x] Thực hiện lệnh Pull (với logic auto stash/merge nếu cần).
- [x] Thực hiện lệnh Push.
- [x] Tự động cập nhật `.gitignore`.

---

## Tasks

- [x] Tạo `backend/services/git_service.go`.
- [x] Tạo `backend/utils/crypto_utils.go` để encrypt/decrypt token.
- [x] Viết hàm `GetBranches(projectDir)`.
- [x] Viết hàm `PullCurrent(projectDir, opts)`.
- [x] Viết hàm `CommitAndPush(projectDir, msg, token)`.
- [x] Viết module đảm bảo `.gitignore` chặn các file nhạy cảm.

---

## Files

- `backend/services/git_service.go`
- `backend/utils/crypto_utils.go`

---

## Test Criteria

- Token được lưu và đọc lại thành công (encrypted).
- Clone 1 repo test, thử thực hiện Pull/Push và đổi branch qua Wails API trả về kết quả đúng định dạng.
