#!/usr/bin/env python3
"""
PatchApplier v3.1 - Ultimate Edition
Designed by: TCO Programmer

Cải tiến v3.1:
- [Feature] Tự động tạo file mới nếu file không tồn tại (New File Creation).
- [Feature] Chức năng Find & Replace (Ctrl + H) giống Notepad.
- [Logic] Cập nhật logic Backup để bỏ qua file mới tạo (không có bản cũ để backup).

Tính năng cốt lõi:
- Patch code thông minh từ nội dung chat.
- Backup & Rollback an toàn.
- Syntax Check & Security Path Traversal Check.
- Giao diện Dark Theme hiện đại.

Refactored to modular structure.
"""

import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont, QPalette
from app.constants import APP_FONT_FAMILY, APP_FONT_SIZE
from app.styles import DARK_STYLESHEET
from app.ui.main_window import PatchApplier

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont(APP_FONT_FAMILY, APP_FONT_SIZE))
    app.setStyleSheet(DARK_STYLESHEET)
    app.setPalette(QPalette())
    
    window = PatchApplier()
    window.show()
    
    sys.exit(app.exec())