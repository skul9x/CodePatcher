from PySide6.QtWidgets import (
    QDialog, QGridLayout, QLabel, QLineEdit, QCheckBox, 
    QHBoxLayout, QPushButton, QMessageBox, QVBoxLayout, QFrame
)
from PySide6.QtGui import QTextDocument, QTextCursor
from PySide6.QtCore import Qt

class FindReplaceDialog(QDialog):
    def __init__(self, parent=None, editor=None):
        super().__init__(parent)
        self.editor = editor
        self.setWindowTitle("Tìm kiếm & Thay thế")
        self.setFixedSize(450, 220)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)
        
        input_frame = QFrame()
        input_frame.setObjectName("Card")
        input_layout = QGridLayout(input_frame)
        input_layout.setContentsMargins(12, 12, 12, 12)
        input_layout.setSpacing(12)
        
        input_layout.addWidget(QLabel("Tìm gì:"), 0, 0)
        self.find_input = QLineEdit()
        input_layout.addWidget(self.find_input, 0, 1)
        
        input_layout.addWidget(QLabel("Thay bằng:"), 1, 0)
        self.replace_input = QLineEdit()
        input_layout.addWidget(self.replace_input, 1, 1)
        
        self.case_sensitive = QCheckBox("Phân biệt Hoa/Thường")
        input_layout.addWidget(self.case_sensitive, 2, 0, 1, 2)
        
        main_layout.addWidget(input_frame)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.btn_find = QPushButton("Tìm tiếp")
        self.btn_replace = QPushButton("Thay thế")
        self.btn_replace_all = QPushButton("Thay tất cả")
        self.btn_replace_all.setProperty("class", "PrimaryButton")
        
        self.btn_cancel = QPushButton("Đóng")
        
        btn_layout.addWidget(self.btn_find)
        btn_layout.addWidget(self.btn_replace)
        btn_layout.addWidget(self.btn_replace_all)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        
        main_layout.addLayout(btn_layout)
        
        self.btn_find.clicked.connect(self.find_next)
        self.btn_replace.clicked.connect(self.replace_one)
        self.btn_replace_all.clicked.connect(self.replace_all)
        self.btn_cancel.clicked.connect(self.close)

    def _get_flags(self):
        flags = QTextDocument.FindFlags()
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        return flags

    def find_next(self):
        text = self.find_input.text()
        if not text: return
        
        found = self.editor.find(text, self._get_flags())
        if not found:
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.editor.setTextCursor(cursor)
            found = self.editor.find(text, self._get_flags())
            
        if not found:
            QMessageBox.information(self, "Thông báo", f"Không tìm thấy '{text}'")

    def replace_one(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            find_text = self.find_input.text()
            selected_text = cursor.selectedText()
            if self.case_sensitive.isChecked():
                match = selected_text == find_text
            else:
                match = selected_text.lower() == find_text.lower()
            if match:
                cursor.insertText(self.replace_input.text())
                self.find_next()
                return
        self.find_next()

    def replace_all(self):
        text = self.find_input.text()
        new_text = self.replace_input.text()
        if not text: return
        
        cursor = self.editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.editor.setTextCursor(cursor)
        
        count = 0
        while self.editor.find(text, self._get_flags()):
            cursor = self.editor.textCursor()
            cursor.insertText(new_text)
            count += 1
            
        QMessageBox.information(self, "Kết quả", f"Đã thay thế {count} vị trí.")