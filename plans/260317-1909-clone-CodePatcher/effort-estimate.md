# Effort Estimation

## Project Size: Small (< 5k LOC)

Dự án gốc là CodePatcher có tổng dung lượng code Python ước tính dưới 2000 LOC, phân bổ qua vài modules đơn giản (UI, Regex Patcher, File I/O, và Git integration).

## Estimation Details

- **Estimated LOC Rewrite**: ~1500 LOC (Go Backend ~800, Frontend JS/TS ~700).
- **Estimated Phases**: 8 phases.
- **Estimated Complexity**: Low - Medium. 
  - *Medium* ở phần xử lý Regex phức tạp của đầu vào block code từ AI.
  - Xử lý Git bằng system calls/exec trên Go khá đơn giản hoặc dùng thư viện `git-go`.
  - Frontend cần thư viện TreeView hoặc component tự code để preview file tree.
- **Estimated AI Sessions**: 2-3 sessions để hoàn thành 100% features.

## Resource & Risks
- **Rủi ro 1**: Regex pattern mapping từ Python (`re`) sang Go (`regexp`). Go `regexp` engine không hỗ trợ các tính năng lookaround (như `(?<=...)` hoặc `(?=...)`). Nếu Regex Python dùng lookaround, sẽ cần viết workaround trên Go. *(Theo mã mẫu `PATCH_REGEX` trong dự án Python, có vẻ khá đơn giản)*
- **Rủi ro 2**: Đảm bảo an toàn thư mục (Path Traversal) khi test đa nền tảng (Windows dùng `\` và Unix dùng `/`). Yêu cầu dùng `path/filepath.Clean` cẩn thận ở Go Backend.
