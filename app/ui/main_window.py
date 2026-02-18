import sys
import os
import shutil
import json
from datetime import datetime

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPlainTextEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QSplitter,
    QLabel, QFileDialog, QMessageBox, QHeaderView, QListWidget, QListWidgetItem,
    QStyle, QProgressDialog, QApplication, QFrame, QStatusBar, QStackedWidget
)
from PySide6.QtGui import (
    QColor, QBrush, QKeySequence, QShortcut, QDesktopServices, QIcon, QFont
)
from PySide6.QtCore import Qt, QSize, QSettings, QTimer, QUrl, QPropertyAnimation, QEasingCurve

from app.constants import (
    APP_TITLE, WINDOW_ICON_NAME, BACKUP_DIR_NAME,
    STATUS_FOUND, STATUS_NEW, STATUS_UNSAFE, PATCH_REGEX
)
from app.utils import is_safe_path, check_syntax
from app.ui.dialogs import FindReplaceDialog
# Import Tab GitHub mới
from app.ui.github_tab import GitHubTab

class PatchApplier(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_dir = ""
        self.patch_content_map = {}
        self.setWindowTitle(APP_TITLE)
        
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, WINDOW_ICON_NAME)))

        try:
            self.script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        except Exception:
            self.script_dir = os.getcwd()
        
        self.backup_root_dir = os.path.join(self.script_dir, BACKUP_DIR_NAME)
        self.settings = QSettings("TCO", "PatchApplier")

        self.debounce_timer = QTimer()
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.parse_and_populate_tree)

        self.initUI()
        self.load_last_directory()
        self.load_history()

    def initUI(self):
        self.setGeometry(100, 100, 1350, 850)
        
        # Central Widget & Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- LEFT SIDEBAR ---
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)

        # App Logo/Title in Sidebar
        logo_sec = QFrame()
        logo_layout = QVBoxLayout(logo_sec)
        app_title_lbl = QLabel("CODE")
        app_title_lbl.setObjectName("HeaderLabel")
        app_title_lbl.setStyleSheet("padding-left: 20px; margin-bottom: 0px;")
        app_subtitle_lbl = QLabel("PATCHER")
        app_subtitle_lbl.setObjectName("HeaderLabel")
        app_subtitle_lbl.setStyleSheet("padding-left: 20px; color: #ECEFF4; font-size: 14pt; margin-top: -10px; margin-bottom: 20px;")
        logo_layout.addWidget(app_title_lbl)
        logo_layout.addWidget(app_subtitle_lbl)
        sidebar_layout.addWidget(logo_sec)

        # Sidebar Buttons
        self.btn_patcher = self.create_sidebar_button("🛠️  Code Patcher", 0)
        self.btn_github = self.create_sidebar_button("☁️  GitHub Sync", 1)
        
        sidebar_layout.addWidget(self.btn_patcher)
        sidebar_layout.addWidget(self.btn_github)
        sidebar_layout.addStretch()

        # Version/User Info at bottom
        version_lbl = QLabel("v3.2 CyberNord")
        version_lbl.setStyleSheet("color: #4C566A; padding-left: 20px; font-size: 8pt;")
        sidebar_layout.addWidget(version_lbl)

        main_layout.addWidget(self.sidebar)

        # --- RIGHT CONTENT AREA ---
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Project Selection (Top Bar in Content Area)
        project_frame = QFrame()
        project_frame.setObjectName("Card")
        project_layout = QHBoxLayout(project_frame)
        project_layout.setContentsMargins(16, 12, 16, 12)
        
        lbl_proj = QLabel("DỰ ÁN:")
        lbl_proj.setObjectName("SubHeader")
        project_layout.addWidget(lbl_proj)
        
        self.project_dir_label = QLabel("Chưa chọn thư mục nào.")
        self.project_dir_label.setStyleSheet("color: #D8DEE9; font-style: italic;")
        project_layout.addWidget(self.project_dir_label, 1)
        
        self.select_folder_button = self.create_button("Chọn Thư mục", "SP_DirOpenIcon", self.select_project_folder)
        self.open_folder_btn = self.create_button("Xem File", "SP_DirIcon", self.open_project_folder)
        
        project_layout.addWidget(self.select_folder_button)
        project_layout.addWidget(self.open_folder_btn)
        
        content_layout.addWidget(project_frame)

        # Stacked Widget for Pages
        self.pages = QStackedWidget()
        content_layout.addWidget(self.pages, 1)

        # === PAGE 1: CODE PATCHER ===
        patcher_page = QWidget()
        patcher_layout = QVBoxLayout(patcher_page)
        patcher_layout.setContentsMargins(0, 0, 0, 0)

        # Splitter (Left: Input/Preview, Right: History)
        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(4)
        patcher_layout.addWidget(splitter, 1)

        # --- Left Panel ---
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 10, 0)
        left_layout.setSpacing(15)

        # Input Card
        input_frame = QFrame()
        input_frame.setObjectName("Card")
        input_box = QVBoxLayout(input_frame)
        input_box.setContentsMargins(15, 15, 15, 15)
        
        top_input_bar = QHBoxLayout()
        lbl_input = QLabel("NỘI DUNG BẢN VÁ")
        lbl_input.setObjectName("SubHeader")
        top_input_bar.addWidget(lbl_input)
        top_input_bar.addStretch()
        
        self.paste_btn = self.create_button("Dán", "SP_ToolBarHorizontalExtensionButton", self.paste_content)
        self.paste_trim_btn = self.create_button("Dán & Lọc", None, self.paste_and_trim_content)
        
        top_input_bar.addWidget(self.paste_btn)
        top_input_bar.addWidget(self.paste_trim_btn)
        input_box.addLayout(top_input_bar)

        self.patch_text_edit = QPlainTextEdit()
        self.patch_text_edit.setPlaceholderText("Dán nội dung code vào đây (Ctrl+V)...\nSử dụng Ctrl+H để Tìm & Thay thế.")
        self.patch_text_edit.textChanged.connect(self._on_patch_text_changed)
        input_box.addWidget(self.patch_text_edit)
        
        left_layout.addWidget(input_frame, 2)

        # Preview Card
        preview_frame = QFrame()
        preview_frame.setObjectName("Card")
        preview_box = QVBoxLayout(preview_frame)
        preview_box.setContentsMargins(15, 15, 15, 15)
        
        lbl_preview = QLabel("XEM TRƯỚC THAY ĐỔI")
        lbl_preview.setObjectName("SubHeader")
        preview_box.addWidget(lbl_preview)

        self.changes_tree = QTreeWidget()
        self.changes_tree.setColumnCount(2)
        self.changes_tree.setHeaderLabels(["File", "Trạng thái"])
        self.changes_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        self.changes_tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        preview_box.addWidget(self.changes_tree)
        
        self.apply_button = self.create_button("TIẾN HÀNH VÁ CODE", "SP_DialogApplyButton", self.apply_changes)
        self.apply_button.setProperty("class", "PrimaryButton")
        self.apply_button.setMinimumHeight(45)
        self.apply_button.setEnabled(False)
        preview_box.addWidget(self.apply_button)
        
        left_layout.addWidget(preview_frame, 3)
        splitter.addWidget(left_container)

        # --- Right Panel: History ---
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(10, 0, 0, 0)
        right_layout.setSpacing(15)
        
        history_frame = QFrame()
        history_frame.setObjectName("Card")
        history_box = QVBoxLayout(history_frame)
        history_box.setContentsMargins(15, 15, 15, 15)
        
        lbl_hist = QLabel("LỊCH SỬ")
        lbl_hist.setObjectName("SubHeader")
        history_box.addWidget(lbl_hist)
        
        self.history_list = QListWidget()
        self.history_list.itemSelectionChanged.connect(self._on_history_selection_changed)
        history_box.addWidget(self.history_list)
        
        action_row = QHBoxLayout()
        self.rollback_button = self.create_button("Hoàn tác", "SP_ArrowLeft", self.rollback_changes)
        self.rollback_button.setEnabled(False)
        self.clear_backups_button = self.create_button("Xóa", "SP_TrashIcon", self.clear_backups, style_class="DangerButton")
        
        action_row.addWidget(self.rollback_button, 1)
        action_row.addWidget(self.clear_backups_button)
        history_box.addLayout(action_row)
        
        right_layout.addWidget(history_frame)
        splitter.addWidget(right_container)
        splitter.setSizes([850, 350])

        self.pages.addWidget(patcher_page)

        # === PAGE 2: GITHUB SYNC ===
        self.github_tab = GitHubTab(self)
        self.pages.addWidget(self.github_tab)

        main_layout.addWidget(content_container, 1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.find_replace_shortcut = QShortcut(QKeySequence("Ctrl+H"), self.patch_text_edit)
        self.find_replace_shortcut.activated.connect(self.open_find_replace_dialog)
        
        # Set Default Page
        self.switch_page(0)

    def create_sidebar_button(self, text, index):
        btn = QPushButton(text)
        btn.setObjectName("SidebarBtn")
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.switch_page(index))
        return btn

    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        # Update sidebar buttons style
        self.btn_patcher.setProperty("active", index == 0)
        self.btn_github.setProperty("active", index == 1)
        
        # Force restyle
        self.btn_patcher.style().unpolish(self.btn_patcher)
        self.btn_patcher.style().polish(self.btn_patcher)
        self.btn_github.style().unpolish(self.btn_github)
        self.btn_github.style().polish(self.btn_github)

    def create_button(self, text, icon_name, on_click, style_class=None):
        btn = QPushButton(text)
        if icon_name:
            icon = self.style().standardIcon(getattr(QStyle, icon_name))
            btn.setIcon(icon)
        if style_class:
            btn.setProperty("class", style_class)
        btn.clicked.connect(on_click)
        return btn

    def show_toast(self, message, is_error=False):
        self.status_bar.showMessage(message, 5000)
        if is_error:
            self.status_bar.setStyleSheet("background-color: #d32f2f; color: white;")
        else:
            self.status_bar.setStyleSheet("background-color: #388e3c; color: white;")
        QTimer.singleShot(5000, lambda: self.status_bar.setStyleSheet(""))

    def open_find_replace_dialog(self):
        dlg = FindReplaceDialog(self, self.patch_text_edit)
        dlg.show()

    def open_project_folder(self):
        if self.project_dir and os.path.exists(self.project_dir):
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.project_dir))
        else:
            self.show_toast("Thư mục dự án không hợp lệ!", True)

    def paste_content(self):
        self.patch_text_edit.clear()
        self.patch_text_edit.paste()

    def paste_and_trim_content(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if not text: return
        new_text = PATCH_REGEX.sub(self._trim_path_callback, text)
        self.patch_text_edit.setPlainText(new_text)
        self.show_toast("Đã dán và lọc đường dẫn")

    def trim_first_directory_from_path(self):
        text = self.patch_text_edit.toPlainText()
        if not text: return
        new_text = PATCH_REGEX.sub(self._trim_path_callback, text)
        if new_text != text:
            self.patch_text_edit.setPlainText(new_text)
            self.show_toast("Đã cắt bớt thư mục đầu tiên trong đường dẫn")
        else:
            self.show_toast("Không tìm thấy đường dẫn nào để cắt", True)

    def _trim_path_callback(self, match):
        full_block = match.group(0)
        content = match.group(1)
        if '\n' in content:
            lines = content.split('\n')
        else:
            lines = [content]
        if not lines: return full_block

        first_line = lines[0].strip()
        if first_line.startswith('#'):
            path_raw = first_line.lstrip('#').strip()
            path_normalized = path_raw.replace('\\', '/')
            parts = path_normalized.split('/')
            
            if len(parts) > 1:
                new_path = "/".join(parts[1:])
                lines[0] = f"# {new_path}"
                start_idx = match.start(1) - match.start(0)
                end_idx = match.end(1) - match.start(0)
                header = full_block[:start_idx]
                footer = full_block[end_idx:]
                new_content = "\n".join(lines)
                return f"{header}{new_content}{footer}"
        return full_block

    def load_last_directory(self):
        last_dir = self.settings.value("last_project_dir", "")
        if last_dir and os.path.exists(last_dir):
            self.project_dir = last_dir
            self.project_dir_label.setText(f"{last_dir}")
            self._on_patch_text_changed()

    def select_project_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Chọn Thư mục Gốc của Dự án")
        if folder:
            self.project_dir = folder
            self.project_dir_label.setText(f"{folder}")
            self.settings.setValue("last_project_dir", folder)
            self._on_patch_text_changed()

    def _on_patch_text_changed(self):
        self.debounce_timer.start(500)

    def parse_and_populate_tree(self):
        self.changes_tree.clear()
        self.patch_content_map.clear()
        
        patch_text = self.patch_text_edit.toPlainText()
        if not self.project_dir:
            self.apply_button.setEnabled(False)
            return

        self.changes_tree.setUpdatesEnabled(False)
        matches = PATCH_REGEX.finditer(patch_text)
        valid_files_count = 0

        for match in matches:
            code_content = match.group(1).strip()
            first_line = code_content.split('\n', 1)[0].strip() if '\n' in code_content else code_content.strip()

            if first_line.startswith('#'):
                file_path_raw = first_line.lstrip('#').strip()
                file_path = os.path.normpath(file_path_raw.replace("\\", "/"))
                
                if not is_safe_path(self.project_dir, file_path):
                    item = QTreeWidgetItem(self.changes_tree)
                    item.setText(0, file_path)
                    item.setText(1, STATUS_UNSAFE)
                    item.setForeground(1, QBrush(QColor("orange")))
                    continue

                if '\n' in code_content:
                    content_without_header = code_content.split('\n', 1)[1].lstrip('\n')
                else:
                    content_without_header = ""
                
                self.patch_content_map[file_path] = content_without_header
                full_target_path = os.path.join(self.project_dir, file_path)
                item = QTreeWidgetItem(self.changes_tree)
                item.setText(0, file_path)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                
                if os.path.exists(full_target_path):
                    item.setText(1, STATUS_FOUND)
                    item.setForeground(1, QBrush(QColor("#4CAF50")))
                    item.setCheckState(0, Qt.Checked)
                    valid_files_count += 1
                else:
                    item.setText(1, STATUS_NEW)
                    item.setForeground(1, QBrush(QColor("#2196F3")))
                    item.setCheckState(0, Qt.Checked)
                    valid_files_count += 1
        
        self.changes_tree.setUpdatesEnabled(True)
        self.apply_button.setEnabled(valid_files_count > 0)

    def apply_changes(self):
        if not self.project_dir: return
        
        # Stop debounce timer để tránh parse_and_populate_tree chạy giữa chừng
        self.debounce_timer.stop()
        
        files_to_patch = []
        for i in range(self.changes_tree.topLevelItemCount()):
            item = self.changes_tree.topLevelItem(i)
            if item.checkState(0) == Qt.Checked and item.text(1) in [STATUS_FOUND, STATUS_NEW]:
                files_to_patch.append(item.text(0))

        if not files_to_patch:
            self.show_toast("Chưa chọn file nào", True)
            return
        
        # Copy patch_content_map để tránh race condition nếu user sửa text
        patch_content_snapshot = dict(self.patch_content_map)

        for file_path in files_to_patch:
            content = patch_content_snapshot.get(file_path)
            is_valid, error_msg = check_syntax(content, file_path)
            if not is_valid:
                reply = QMessageBox.warning(
                    self, "Lỗi Cú pháp",
                    f"File '{file_path}' có lỗi:\n{error_msg}\n\nBạn có muốn tiếp tục không?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No
                )
                if reply == QMessageBox.No: return
        
        # Disable các controls khi đang apply
        self.apply_button.setEnabled(False)
        self.patch_text_edit.setEnabled(False)

        batch_id = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_batch_dir = os.path.join(self.backup_root_dir, batch_id)
        
        progress = QProgressDialog("Đang áp dụng bản vá...", "Hủy", 0, len(files_to_patch), self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)
        
        try:
            os.makedirs(backup_batch_dir, exist_ok=True)
            patched_files_list = []
            
            for i, file_path in enumerate(files_to_patch):
                progress.setValue(i)
                if progress.wasCanceled(): break

                full_target_path = os.path.join(self.project_dir, file_path)
                full_backup_path = os.path.join(backup_batch_dir, file_path)
                
                file_exists = os.path.exists(full_target_path)
                if file_exists:
                    backup_dir = os.path.dirname(full_backup_path)
                    if backup_dir:
                        os.makedirs(backup_dir, exist_ok=True)
                    shutil.copy2(full_target_path, full_backup_path)
                
                os.makedirs(os.path.dirname(full_target_path), exist_ok=True)

                new_content = patch_content_snapshot.get(file_path)
                if new_content is not None:
                    with open(full_target_path, 'w', encoding='utf-8', newline='\n') as f:
                        f.write(new_content)
                    patched_files_list.append(file_path)

            progress.setValue(len(files_to_patch))

            manifest_path = os.path.join(backup_batch_dir, "manifest.json")
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "project_dir": self.project_dir,
                    "patched_files": patched_files_list
                }, f, indent=2)

            self.update_history_list(batch_id, patched_files_list, self.project_dir)
            self.show_toast(f"Thành công! Đã vá {len(patched_files_list)} file.")
            
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Thất bại: {e}")
            self.load_history()
        finally:
            # Re-enable controls sau khi hoàn thành
            self.patch_text_edit.setEnabled(True)
            self._on_patch_text_changed()  # Trigger lại parse để cập nhật trạng thái

    def rollback_changes(self):
        selected = self.history_list.selectedItems()
        if not selected:
            self.show_toast("Chưa chọn mục nào để hoàn tác!", True)
            return
        item = selected[0]
        batch_id = item.data(Qt.UserRole)
        backup_batch_dir = os.path.join(self.backup_root_dir, batch_id)
        manifest_path = os.path.join(backup_batch_dir, "manifest.json")

        if not os.path.exists(manifest_path):
            self.show_toast("Thiếu file Manifest!", True)
            return

        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            project_dir = data.get("project_dir")
            files = data.get("patched_files", [])

            if not os.path.exists(project_dir):
                self.show_toast("Không tìm thấy thư mục gốc", True)
                return

            if QMessageBox.question(self, "Xác nhận", f"Hoàn tác đợt vá '{batch_id}'?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.No:
                return

            progress = QProgressDialog("Đang hoàn tác...", "Hủy", 0, len(files), self)
            progress.setWindowModality(Qt.WindowModal)
            
            count = 0
            for i, rel_path in enumerate(files):
                progress.setValue(i)
                backup_path = os.path.join(backup_batch_dir, rel_path)
                target_path = os.path.join(project_dir, rel_path)
                
                if os.path.exists(backup_path):
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(backup_path, target_path)
                    count += 1
                else:
                    if os.path.exists(target_path):
                        try:
                            os.remove(target_path)
                            count += 1
                        except: pass
            
            progress.setValue(len(files))
            
            data["rolled_back"] = True
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
                
            item.setText(item.text() + "\n(Đã hoàn tác)")
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            item.setForeground(QBrush(QColor("#666")))
            self.rollback_button.setEnabled(False)
            
            self.show_toast(f"Hoàn tác xong: {count} file đã khôi phục")

        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Hoàn tác thất bại: {e}")

    def update_history_list(self, batch_id, files, project_dir, rolled_back=False):
        files_str = ", ".join(files)
        if len(files_str) > 60: files_str = files_str[:60] + "..."
        text = f"{batch_id} | {os.path.basename(project_dir)}\n{files_str}"
        if rolled_back: text += "\n(Đã hoàn tác)"
        
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, batch_id)
        item.setToolTip(f"Đường dẫn: {project_dir}\nFiles: {files}")
        
        if rolled_back:
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            item.setForeground(QBrush(QColor("#666")))
            
        self.history_list.insertItem(0, item)

    def load_history(self):
        self.history_list.clear()
        if not os.path.exists(self.backup_root_dir): return
        
        for batch_id in sorted(os.listdir(self.backup_root_dir), reverse=True):
            path = os.path.join(self.backup_root_dir, batch_id)
            if os.path.isdir(path):
                mf = os.path.join(path, "manifest.json")
                if os.path.exists(mf):
                    try:
                        with open(mf, 'r', encoding='utf-8') as f:
                            d = json.load(f)
                        self.update_history_list(batch_id, d.get("patched_files", []), d.get("project_dir", ""), d.get("rolled_back", False))
                    except: pass

    def _on_history_selection_changed(self):
        items = self.history_list.selectedItems()
        self.rollback_button.setEnabled(bool(items and (items[0].flags() & Qt.ItemIsEnabled)))

    def clear_backups(self):
        if os.path.exists(self.backup_root_dir) and QMessageBox.warning(self, "Cảnh báo", "Xóa vĩnh viễn toàn bộ bản sao lưu (backup)?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            shutil.rmtree(self.backup_root_dir)
            self.history_list.clear()
            self.rollback_button.setEnabled(False)
            self.show_toast("Đã xóa sạch lịch sử")