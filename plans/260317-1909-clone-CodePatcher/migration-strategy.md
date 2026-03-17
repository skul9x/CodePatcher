# Migration Strategy

## Approach: Direct Rewrite (với Separation of Concerns)

Vì kích thước codebase của dự án gốc khá nhỏ (dưới 5k LOC, cụ thể khoảng 1k-2k LOC), chiến lược **Direct Rewrite** (Viết lại toàn bộ) là phù hợp và hiệu quả nhất. Không cần thiết áp dụng Strangler Pattern hay Incremental Migration phức tạp.

## Key Principles for Rewrite

1. **Decoupling UI and Logic**:
   - Tách biệt hoàn toàn phần giao diện (UI) và logic nghiệp vụ.
   - Core logic (đọc/ghi file, check path an toàn, parse regex, gọi Git) sẽ được viết bằng Go và expose qua Wails Bindings.
   - Frontend (React/Vite) chỉ đảm nhiệm việc gọi API từ Bindings và hiển thị trạng thái, xử lý user interaction (Debounce input, TreeView).

2. **Feature Parity**:
   - Đảm bảo giữ nguyên các chức năng (Feature) như file `features.md`.
   - Các pattern regex (trong `constants.py`) cần được bê nguyên xi sang Go `regexp` package.
   - Logic backup/rollback cần tái tạo chính xác cơ chế tạo batch folder và file `manifest.json`.

3. **Multi-platform build**:
   - Sử dụng Wails CLI để build cho Windows (`.exe` với icon) và Ubuntu 24.04 (`.deb` hoặc binary).
   - Go OS system calls (I/O) đã hỗ trợ cross-platform mặc định. Tuy nhiên, các thao tác xử lý đường dẫn (`path/filepath` trong cài đặt) cần cẩn thận giữ tính nhất quán đa nền tảng.

## Steps to Execute
1. Khởi tạo template `wails init` với frontend framwork (React/Preact/Svelte tùy chọn).
2. Xây dựng Core Go Services (Config, Patcher, Git, Backup/Rollback).
3. Xây dựng Frontend UI tương ứng (Patcher Tab, GitHub Tab).
4. Tích hợp Wails Bindings.
5. Kiểm thử tích hợp đa nền tảng (Build cho Windows/Ubuntu).
