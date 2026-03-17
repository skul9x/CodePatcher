# Features Extracted from CodePatcher v3.1

## 1. Code Patching (Khâu vá code)
- **Input Parsing**: Nhận text đầu vào chứa các khối code. Sử dụng Regex để parse đường dẫn file và nội dung.
- **Path Processing**: Chức năng "Dán & Xóa path đầu", "Xóa Path (Thủ công)" để chuẩn hóa đường dẫn.
- **Security Check**: Kiểm tra Path Traversal (`is_safe_path`) để tránh ghi đè file ngoài dự án.
- **Syntax Check**: Kiểm tra lỗi cú pháp của code trước khi apply (`check_syntax`).
- **Dry Run (Preview)**: Hiển thị danh sách file sẽ bị ảnh hưởng dưới dạng TreeView (Đường dẫn File, Trạng thái: STATUS_FOUND, STATUS_NEW, STATUS_UNSAFE).
- **Apply Patch**: Thực hiện ghi đè nội dung mới vào các file đã chọn. Tạo file mới nếu chưa tồn tại.
- **Backup & Rollback**: 
  - Tự động backup file gốc trước khi apply patch vào thư mục `backups/{batch_id}`.
  - Tạo `manifest.json` ghi lại lịch sử.
  - Chức năng Rollback (Hoàn tác) dựa trên lịch sử đợt vá.

## 2. GitHub Sync (Đồng bộ GitHub)
- **Token Management**: Nhập token, mã hóa và lưu trữ an toàn (`TokenCipher`).
- **Repository Connection**: Kết nối tới Remote Git repo.
- **Auto Sync**: 1-click Pull, Merge, và Push.
- **Branch Management**: Liệt kê branch, tạo branch mới, chuyển branch, xóa branch.
- **Gitignore Management**: Tự động quản lý `.gitignore` để ẩn các file nhạy cảm/không cần thiết.

## 3. UI/UX Enhancements
- **Dark Theme**: Giao diện tối hiện đại.
- **Find & Replace**: Tính năng tìm kiếm và thay thế như Notepad (Ctrl+H).
- **Toast Notifications**: Thanh trạng thái hiển thị thông báo.
- **Debounce Parsing**: Tự động parse code sau khi ngừng gõ 500ms.
- **History List**: Xem lịch sử các đợt áp dụng bản vá.
