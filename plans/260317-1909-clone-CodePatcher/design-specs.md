# Design Specifications: CodePatcher-Go

## 🎨 Vibe & Concept
- **Phong cách:** Developer-focused, siêu tối giản (Dark Mode) giống VS Code, Cursor.
- **Trải nghiệm:** Tốc độ nhanh, không nhồi nhét hiệu ứng dư thừa. Ưu tiên dễ nhìn khối code, lịch sử lỗi.
- **Cảm hứng:** VS Code, Vercel Dashboard (tối giản box-shadow).

## 🎨 Color Palette
| Name | Hex | Usage |
|------|-----|-------|
| Background | `#1e1e1e` | Nền chính của App (VS Code Default bg) |
| Surface | `#252526` | Nền của các Panel phụ (Sidebar, Header, Cards) |
| Border | `#3c3c3c` | Đường phân cách Splitter, viền thẻ |
| Primary | `#0e639c` | Nút chức năng chính (Xanh lam VS Code) |
| Primary Hover | `#1177bb` | Hover state của nút chính |
| Success | `#4CAF50` | Nút Apply thành công, Icon tích xanh |
| Danger | `#f14c4c` | Nút Rollback, Xóa Backups, Lỗi Syntax |
| Warning | `#cca700` | Cảnh báo path không an toàn |
| Text Main | `#cccccc` | Chữ đọc thông thường |
| Text Muted | `#858585` | Chữ ghi chú, label phụ, path dài |

## 📝 Typography
- **Font Stack:** `Inter, system-ui, sans-serif` (dễ đọc, quốc dân).
- **Code Font:** `JetBrains Mono, Fira Code, Consolas` cho các đoạn code input, terminal tab.
| Element | Font | Size | Weight |
|---------|------|------|--------|
| Header | Inter | 16px | 600 (Semibold) |
| Body | Inter | 14px | 400 (Regular) |
| Code | JetBrains | 13px | 400 |
| Small Text | Inter | 12px | 400 |

## 📐 Spacing System (Compact)
| Name | Value | Usage |
|------|-------|-------|
| xs | 4px | Khe Icon và text |
| sm | 8px | Margin giữa các List elements |
| md | 12px | Padding viền trong Cards |
| lg | 16px | Khoảng cách các vùng lớn (Panels) |

## 🔲 Border Radius
| Name | Value | Usage |
|------|-------|-------|
| none | 0px | Các panel dính liền Splitter |
| sm | 4px | Buttons, Inputs, Checkboxes |
| md | 6px | Thẻ Card nội dung rời |

## 🌫️ Shadows & Interactions
- **Shadows:** Bỏ các hộp bóng bẩy. Dùng border `1px solid #3c3c3c` để phân tách mảng 2D.
- **Interaction:** Cực kỳ đơn giản.
  - Button chỉ sáng màu hoặc viền nhấn nhẹ khi Hover.
  - Active Button lặn xuống tý xíu (ấn `transform: scale(0.98)`).
  - Không có hiệu ứng Slide/Fade/Zoom phức tạp để tiết kiệm resource và tạo cảm giác Snappy.

## 📱 Breakpoints
- Windows App cố định tối thiểu: `1000px x 600px` (có thể thu nhỏ Splitter Panels).
- Không cần responsive cho Mobile layout do là Tool gõ phím Desktop.

## 🖼️ Component Specs
- **Split Pane:** Đường kéo thả xám `#3c3c3c`, Hover lên thì chuyển `#007acc` dầy 2px.
- **Giao diện:** Tối giản, chuyên nghiệp, hỗ trợ tiếng Việt toàn diện.
- **TreeView:** Không bọc khối, icon thư mục nhỏ trước tên, Text File. Click chọn thì highlight dòng `#04395e`. Trạng thái có icon Checkmark bên cạnh.
- **Terminal Log:** Box cuộn độc lập, font chữ Code xanh hacker dội ra nền `#000000` nhám.
- **Tabs:** Active tab gạch dưới dầy 2px màu '#007acc', Inactive tab chữ '#858585' và nền đồng bộ.
