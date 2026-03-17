# Architecture Detection

## Current Architecture: Layered MVC (Desktop)

Dự án Python hiện tại sử dụng kiến trúc phân lớp cơ bản cho Desktop application:

1. **Presentation Layer (UI)**: 
   - Xây dựng bằng PySide6.
   - Chứa logic hiển thị và handle events (e.g. `main_window.py`, `github_tab.py`).
   - Coupling khá chặt chẽ với logic xử lý file và UI update (ví dụ hàm `apply_changes` thực hiện cả I/O backup và logic update UI trực tiếp).

2. **Business/Core Layer**:
   - `git_core.py`: Xử lý domain logic về Git sử dụng thư viện bên thứ 3 (GitPython).
   - `utils.py`: Chứa Pure Functions cho cryptography và validation.

3. **Data/Persistence Layer**:
   - Lịch sử backup lưu trực tiếp trên File System (`backups/`).
   - Cấu hình lưu qua `QSettings` (Registry trên Windows, file config trên Ubuntu).

## Proposed Architecture for Go (Wails v2)

Kiến trúc mới sẽ sử dụng **Wails v2** (Client-Server model over IPC):

1. **Frontend (Presentation)**:
   - React/Vite (hoặc Vue/Svelte).
   - Quản lý State bằng React Hooks (hoặc trạng thái tương đương).
   - Gọi Backend qua các Wails Bindings.

2. **Backend (Go Services)**:
   - `App` struct làm entry point cho Wails.
   - `PatchService`: Xử lý logic đọc, ghi, backup, rollback, regex parsing.
   - `GitService`: Xử lý Git operations bằng thư viện `go-git` (hoặc gọi git CLI qua `os/exec`).
   - `ConfigService`: Quản lý lưu trữ token và project paths.

3. **Data Layer**:
   - File System cho backup (như cũ).
   - JSON file hoặc kho lưu trữ keyring an toàn để lưu cấu hình thay vì `QSettings`.

### Coupling Issues in Original Code rủi ro khi Migrate:
- Python UI trực tiếp thao tác File I/O => Trong Go, Frontend chỉ UI, mọi thao tác I/O phải đẩy qua Go functions.
- Python `QSettings` => Phải thay thế bằng Go mechanism lưu settings (như config YAML/JSON tại app data).
