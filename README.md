# CodePatcher Pro - Công cụ Áp dụng Bản vá AI siêu tốc 🚀

**CodePatcher Pro** là một ứng dụng Desktop mạnh mẽ được viết bằng **Go (Wails v2)** và **React**, giúp các lập trình viên áp dụng nhanh chóng các đoạn mã (code blocks) được tạo ra bởi AI (như ChatGPT, Claude) vào mã nguồn hiện tại một cách an toàn và thông minh.

## 🌟 Tính năng chính

- **Vá mã thông minh (Smart Patching):** Tự động phát hiện đường dẫn tệp từ các khối mã Markdown (`# path/to/file`) và ghi đè nội dung chính xác.
- **Sao lưu & Hoàn tác (Backup & Rollback):** Tự động tạo bản sao lưu trước khi thay đổi bất kỳ tệp nào. Bạn có thể hoàn tác (Rollback) 1-click về trạng thái trước đó nếu có lỗi.
- **Đồng bộ GitHub:** Tích hợp các thao tác Git cơ bản như Pull, Commit và Push trực tiếp ngay trong ứng dụng.
- **Giao diện hiện đại (VS Code Vibe):** Giao diện tối giản, tối ưu hóa cho lập trình viên với khả năng kéo giãn layout linh hoạt.
- **Bảo mật:** Hỗ trợ xác thực GitHub qua Token (PAT).
- **Đa nền tảng:** Hỗ trợ Windows và Linux.

## 🚀 Hướng dấn cài đặt

### Yêu cầu hệ thống
- **Go:** v1.22.2 hoặc mới hơn.
- **Node.js:** v16+ và npm.
- **Wails v2:** Cài đặt qua `go install github.com/wailsapp/wails/v2/cmd/wails@latest`.

### Cài đặt từ mã nguồn
1. Clone repository:
   ```bash
   git clone https://github.com/skul9x/CodePatcher.git
   cd CodePatcher-Go
2. Cài đặt dependencies:
   ```bash
   go mod tidy
   cd frontend && npm install && cd ..
3. Chạy ứng dụng ở chế độ phát triển:
   ```bash
   wails dev
   ```

## 🛠️ Hướng dẫn sử dụng

1. **Chọn thư mục dự án:** Nhấp vào "Chọn thư mục..." ở thanh tiêu đề để chọn project bạn muốn vá mã.
2. **Dán mã AI:** Copy nội dung phản hồi từ AI (có chứa các block mã) và dán vào tab "Trình Vá Mã".
3. **Áp dụng:** Nhấn "Áp Dụng Bản Vá". Ứng dụng sẽ tự động sao lưu các file bị ảnh hưởng và ghi đè nội dung mới.
4. **Hoàn tác:** Nếu muốn quay lại, hãy kiểm tra danh sách "Lịch Sử Gần Đây" và nhấn nút hoàn tác bên cạnh đợt vá đó.
5. **Đồng bộ:** Chuyển sang tab "Đồng Bộ GitHub" để đẩy các thay đổi lên repository của bạn.

## 🏗️ Hướng dẫn Build

### Windows
Để build file `.exe` và bộ cài đặt:
```bash
wails build -platform windows/amd64 -nsis
```

### Linux
Để build file thực thi và gói `.deb`:
```bash
wails build -platform linux/amd64
# (Sử dụng các công cụ như dpkg-deb để đóng gói nếu cần)
```

## 📂 Cấu trúc thư mục

```text
.
├── main.go            # Điểm khởi đầu ứng dụng
├── app.go             # Cầu nối (Bindings) Backend & Frontend
├── backend/           # Logic nghiệp vụ (Go)
│   ├── services/      # Các dịch vụ Git, Backup, Parser
│   └── models/        # Định nghĩa dữ liệu
├── frontend/          # Giao diện người dùng (React + TS)
│   ├── src/           # Source code UI
│   └── wailsjs/       # Các bindings tự động sinh bởi Wails
├── build/             # Chứa các file sau khi build
└── .brain/            # Lưu trữ tri thức và trạng thái dự án
```

## 🤝 Đóng góp
Mọi đóng góp đều được trân trọng. Vui lòng tạo Issue hoặc Pull Request nếu bạn có ý tưởng cải tiến!

---
*Phát triển bởi Antigravity AI với 💙*
