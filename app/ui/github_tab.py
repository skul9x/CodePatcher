from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QTextEdit, QMessageBox, QProgressBar, 
    QCheckBox, QScrollArea
)
from PySide6.QtCore import Qt, QThread, Signal, QSettings
from datetime import datetime
from app.git_core import GitManager
from app.utils import TokenCipher

class GitWorkerThread(QThread):
    finished_signal = Signal(bool, str)

    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

    def run(self):
        success, msg = self.func(*self.args)
        self.finished_signal.emit(success, msg)

class GitHubTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.git_manager = None
        self.connected_project_dir = None  # Lưu thư mục đã connect để verify
        self.settings = QSettings("TCO", "PatchApplier")
        self.initUI()
        self.load_settings()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(20)

        settings_frame = QFrame()
        settings_frame.setObjectName("Card")
        s_layout = QVBoxLayout(settings_frame)
        s_layout.setContentsMargins(20, 20, 20, 20)
        s_layout.setSpacing(16)
        
        lbl_setup = QLabel("Cấu hình Repository")
        lbl_setup.setObjectName("HeaderLabel")
        s_layout.addWidget(lbl_setup)
        
        vbox_repo = QVBoxLayout()
        vbox_repo.setSpacing(6)
        vbox_repo.addWidget(QLabel("URL GitHub:"))
        self.repo_input = QLineEdit()
        self.repo_input.setPlaceholderText("VD: https://github.com/username/repo.git")
        vbox_repo.addWidget(self.repo_input)
        s_layout.addLayout(vbox_repo)

        vbox_token = QVBoxLayout()
        vbox_token.setSpacing(6)
        vbox_token.addWidget(QLabel("Personal Access Token:"))
        
        token_row = QHBoxLayout()
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("Dán Token bắt đầu bằng ghp_... hoặc github_pat_...")
        self.token_input.setEchoMode(QLineEdit.Password)
        token_row.addWidget(self.token_input)
        
        self.btn_toggle_token = QPushButton("👁")
        self.btn_toggle_token.setFixedWidth(40)
        self.btn_toggle_token.setToolTip("Hiện/Ẩn Token")
        self.btn_toggle_token.clicked.connect(self.toggle_token_visibility)
        token_row.addWidget(self.btn_toggle_token)
        vbox_token.addLayout(token_row)
        
        self.chk_save_token = QCheckBox("Lưu Token (Mã hóa)")
        self.chk_save_token.setChecked(True)
        vbox_token.addWidget(self.chk_save_token)
        s_layout.addLayout(vbox_token)
        
        vbox_branch = QVBoxLayout()
        vbox_branch.setSpacing(6)
        vbox_branch.addWidget(QLabel("Branch:"))
        
        branch_row = QHBoxLayout()
        self.branch_input = QLineEdit("main")
        branch_row.addWidget(self.branch_input)
        
        self.btn_switch_branch = QPushButton("Sử dụng / Tạo mới")
        self.btn_switch_branch.setCursor(Qt.PointingHandCursor)
        self.btn_switch_branch.setEnabled(False)
        self.btn_switch_branch.clicked.connect(self.do_switch_branch)
        branch_row.addWidget(self.btn_switch_branch)
        
        self.btn_delete_branch = QPushButton("Xóa")
        self.btn_delete_branch.setCursor(Qt.PointingHandCursor)
        self.btn_delete_branch.setProperty("class", "DangerButton")
        self.btn_delete_branch.setToolTip("Xóa branch này trên GitHub")
        self.btn_delete_branch.setEnabled(False)
        self.btn_delete_branch.clicked.connect(self.do_delete_branch)
        branch_row.addWidget(self.btn_delete_branch)
        
        vbox_branch.addLayout(branch_row)
        s_layout.addLayout(vbox_branch)

        # Hiển thị thư mục đang sync
        self.current_dir_label = QLabel("Chưa kết nối thư mục nào")
        self.current_dir_label.setStyleSheet("color: #4C566A; font-style: italic; padding: 10px; background: #2E3440; border: 1px solid #4C566A; border-radius: 4px;")
        s_layout.addWidget(self.current_dir_label)

        self.btn_connect = QPushButton("Kết nối / Khởi tạo Git")
        self.btn_connect.setCursor(Qt.PointingHandCursor)
        self.btn_connect.clicked.connect(self.connect_git)
        s_layout.addWidget(self.btn_connect)

        content_layout.addWidget(settings_frame)

        actions_frame = QFrame()
        actions_frame.setObjectName("Card")
        a_layout = QVBoxLayout(actions_frame)
        a_layout.setContentsMargins(20, 20, 20, 20)
        a_layout.setSpacing(16)
        
        lbl_action = QLabel("Thao tác")
        lbl_action.setObjectName("HeaderLabel")
        a_layout.addWidget(lbl_action)
        
        btn_row = QHBoxLayout()
        btn_row.setSpacing(16)
        
        self.btn_pull = QPushButton("⬇ Pull")
        self.btn_pull.setProperty("class", "SuccessButton")
        self.btn_pull.setCursor(Qt.PointingHandCursor)
        self.btn_pull.clicked.connect(self.do_pull)
        self.btn_pull.setEnabled(False)
        
        self.btn_push = QPushButton("⬆ Force Push")
        self.btn_push.setProperty("class", "PrimaryButton")
        self.btn_push.setCursor(Qt.PointingHandCursor)
        self.btn_push.clicked.connect(self.do_push)
        self.btn_push.setEnabled(False)

        self.btn_sync = QPushButton("🔄 Pull-Merge-Push")
        self.btn_sync.setProperty("class", "SecondaryButton")
        self.btn_sync.setCursor(Qt.PointingHandCursor)
        self.btn_sync.clicked.connect(self.do_pull_merge_push)
        self.btn_sync.setEnabled(False)
        self.btn_sync.setToolTip("Đồng bộ an toàn: Pull code từ remote, merge với local, rồi push (không ghi đè)")

        self.btn_rollback = QPushButton("↩ Undo Push")
        self.btn_rollback.setProperty("class", "DangerButton")
        self.btn_rollback.setCursor(Qt.PointingHandCursor)
        self.btn_rollback.clicked.connect(self.do_rollback)
        self.btn_rollback.setEnabled(False)
        
        btn_row.addWidget(self.btn_pull)
        btn_row.addWidget(self.btn_push)
        btn_row.addWidget(self.btn_sync)
        btn_row.addWidget(self.btn_rollback)
        a_layout.addLayout(btn_row)
        
        vbox_msg = QVBoxLayout()
        vbox_msg.setSpacing(6)
        vbox_msg.addWidget(QLabel("Nội dung Commit:"))
        self.commit_msg_input = QLineEdit()
        self.commit_msg_input.setPlaceholderText("Nhập nội dung thay đổi (để trống sẽ tự sinh)")
        vbox_msg.addWidget(self.commit_msg_input)
        a_layout.addLayout(vbox_msg)
        
        content_layout.addWidget(actions_frame)

        vbox_log = QVBoxLayout()
        vbox_log.setSpacing(6)
        vbox_log.addWidget(QLabel("Nhật ký Git:"))
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setPlaceholderText("Trạng thái lệnh Git sẽ hiển thị tại đây...")
        self.log_area.setMaximumHeight(150)
        self.log_area.setMinimumHeight(100)
        vbox_log.addWidget(self.log_area)
        
        content_layout.addLayout(vbox_log)

        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        self.progress.setFixedHeight(4)
        main_layout.addWidget(self.progress)

    def toggle_token_visibility(self):
        if self.token_input.echoMode() == QLineEdit.Password:
            self.token_input.setEchoMode(QLineEdit.Normal)
            self.btn_toggle_token.setText("🙈")
        else:
            self.token_input.setEchoMode(QLineEdit.Password)
            self.btn_toggle_token.setText("👁")

    def log(self, msg, color="#ffffff"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.append(f'<span style="color:#666">[{timestamp}]</span> <span style="color:{color}">{msg}</span>')
        self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

    def load_settings(self):
        repo = self.settings.value("git_repo", "")
        branch = self.settings.value("git_branch", "main")
        enc_token = self.settings.value("git_token_enc", "")
        
        if repo: self.repo_input.setText(repo)
        if branch: self.branch_input.setText(branch)
        
        if enc_token:
            token = TokenCipher.decrypt(enc_token)
            if token:
                self.token_input.setText(token)
                self.chk_save_token.setChecked(True)

    def save_settings(self):
        self.settings.setValue("git_repo", self.repo_input.text().strip())
        self.settings.setValue("git_branch", self.branch_input.text().strip())
        
        if self.chk_save_token.isChecked():
            token = self.token_input.text().strip()
            if token:
                enc_token = TokenCipher.encrypt(token)
                self.settings.setValue("git_token_enc", enc_token)
        else:
            self.settings.remove("git_token_enc")

    def connect_git(self):
        project_dir = self.main_window.project_dir
        if not project_dir:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn thư mục dự án ở tab Patch trước!")
            return

        url = self.repo_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập URL GitHub!")
            return

        self.save_settings()
        self.git_manager = GitManager(project_dir)
        self.connected_project_dir = project_dir  # Lưu lại thư mục đã connect
        
        ok, msg = self.git_manager.init_or_load_repo()
        if ok:
            self.log(f"✅ {msg}", "#4CAF50")
            ok_remote, msg_remote = self.git_manager.set_remote(url)
            if ok_remote:
                self.log(f"✅ {msg_remote}", "#4CAF50")
                self.btn_pull.setEnabled(True)
                self.btn_push.setEnabled(True)
                self.btn_sync.setEnabled(True)
                self.btn_rollback.setEnabled(True)
                self.btn_switch_branch.setEnabled(True)
                self.btn_delete_branch.setEnabled(True)
                self.btn_connect.setText("Kết nối lại")
                # Cập nhật label hiển thị thư mục đang sync
                self.current_dir_label.setText(f"📁 Đang sync: {project_dir}")
                self.current_dir_label.setStyleSheet("color: #A3BE8C; font-weight: bold; padding: 10px; background: #2E3440; border: 1px solid #A3BE8C; border-radius: 4px;")
            else:
                self.log(f"❌ {msg_remote}", "#d32f2f")
        else:
            self.log(f"❌ {msg}", "#d32f2f")

    def _verify_project_dir(self):
        """Verify thư mục hiện tại khớp với thư mục đã connect."""
        current_dir = self.main_window.project_dir
        if not self.connected_project_dir:
            return False, "Chưa kết nối Git. Vui lòng nhấn 'Kết nối / Khởi tạo Git' trước."
        if current_dir != self.connected_project_dir:
            return False, (f"⚠️ Thư mục đã thay đổi!\n\n"
                          f"Đang sync: {self.connected_project_dir}\n"
                          f"Thư mục hiện tại: {current_dir}\n\n"
                          f"Vui lòng nhấn 'Kết nối lại' để cập nhật.")
        return True, ""

    def run_git_task(self, func, *args):
        # Kiểm tra nếu đang có task chạy
        if hasattr(self, 'worker') and self.worker is not None and self.worker.isRunning():
            QMessageBox.warning(self, "Đang xử lý", "Vui lòng đợi thao tác hiện tại hoàn thành.")
            return
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.btn_pull.setEnabled(False)
        self.btn_push.setEnabled(False)
        self.btn_sync.setEnabled(False)
        self.btn_rollback.setEnabled(False)
        self.btn_connect.setEnabled(False)
        
        # Disconnect signal từ worker cũ nếu có để tránh duplicate handlers
        if hasattr(self, 'worker') and self.worker is not None:
            try:
                self.worker.finished_signal.disconnect(self.on_task_finished)
            except (TypeError, RuntimeError):
                pass  # Signal chưa được connect hoặc đã disconnect
        
        self.worker = GitWorkerThread(func, *args)
        self.worker.finished_signal.connect(self.on_task_finished)
        self.worker.start()

    def on_task_finished(self, success, msg):
        self.progress.setVisible(False)
        self.btn_pull.setEnabled(True)
        self.btn_push.setEnabled(True)
        self.btn_sync.setEnabled(True)
        self.btn_rollback.setEnabled(True)
        self.btn_connect.setEnabled(True)
        if success:
            self.log(f"✅ {msg}", "#4CAF50")
            QMessageBox.information(self, "Thành công", msg)
            self.save_settings()
        else:
            self.log(f"❌ {msg}", "#d32f2f")
            QMessageBox.critical(self, "Lỗi Git", msg)

    def do_pull(self):
        # Verify thư mục trước khi thao tác
        ok, err_msg = self._verify_project_dir()
        if not ok:
            QMessageBox.warning(self, "Lỗi", err_msg)
            return
        
        # Cảnh báo vì Pull sẽ xóa uncommitted changes
        reply = QMessageBox.warning(
            self, "Xác nhận Pull", 
            "CẢNH BÁO: Thao tác Pull sẽ:\n"
            "• Tải code từ GitHub về máy\n"
            "• GHI ĐÈ toàn bộ thay đổi chưa commit\n\n"
            "Bạn có chắc chắn muốn tiếp tục?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No: return
        
        self.save_settings()
        token = self.token_input.text().strip()
        branch = self.branch_input.text().strip() or "main"
        
        self.log(f"⏳ Đang Pull từ branch '{branch}'...", "#2196F3")
        self.run_git_task(self.git_manager.pull_code, token, branch)

    def do_push(self):
        # Verify thư mục trước khi thao tác
        ok, err_msg = self._verify_project_dir()
        if not ok:
            QMessageBox.warning(self, "Lỗi", err_msg)
            return
        
        self.save_settings()
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Thiếu Token", "Bạn cần nhập Github Personal Access Token để Push!")
            return
        
        msg = self.commit_msg_input.text().strip() or "Auto update from CodePatcher"
        branch = self.branch_input.text().strip() or "main"
        repo_url = self.repo_input.text().strip()
        project_dir = self.connected_project_dir or self.main_window.project_dir
        
        # Cảnh báo vì Push là force push
        reply = QMessageBox.warning(
            self, "Xác nhận Force Push", 
            f"⚠️ FORCE PUSH sẽ GHI ĐÈ code trên GitHub!\n\n"
            f"📁 Thư mục: {project_dir}\n"
            f"🔗 GitHub: {repo_url}\n"
            f"🌿 Branch: {branch}\n"
            f"📝 Commit: {msg}\n\n"
            f"Bạn có chắc chắn muốn tiếp tục?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No: return
        
        self.log(f"⏳ Đang Push lên branch '{branch}'...", "#2196F3")
        self.run_git_task(self.git_manager.push_code, token, msg, branch)

    def do_pull_merge_push(self):
        # Verify thư mục trước khi thao tác
        ok, err_msg = self._verify_project_dir()
        if not ok:
            QMessageBox.warning(self, "Lỗi", err_msg)
            return
        
        self.save_settings()
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Thiếu Token", "Bạn cần nhập Github Personal Access Token!")
            return
        
        msg = self.commit_msg_input.text().strip() or "Auto update from CodePatcher"
        branch = self.branch_input.text().strip() or "main"
        repo_url = self.repo_input.text().strip()
        project_dir = self.connected_project_dir or self.main_window.project_dir
        
        reply = QMessageBox.information(
            self, "Xác nhận Pull-Merge-Push", 
            f"Đồng bộ AN TOÀN (không ghi đè):\n\n"
            f"📁 Thư mục: {project_dir}\n"
            f"🔗 GitHub: {repo_url}\n"
            f"🌿 Branch: {branch}\n"
            f"📝 Commit: {msg}\n\n"
            f"Quy trình:\n"
            f"1️⃣ Commit local changes\n"
            f"2️⃣ Pull từ GitHub\n"
            f"3️⃣ Merge với local\n"
            f"4️⃣ Push lên GitHub\n\n"
            f"⚠️ Nếu có conflict, thao tác sẽ bị hủy.\n\n"
            f"Bạn có muốn tiếp tục?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        if reply == QMessageBox.No: return
        
        self.log(f"⏳ Đang Pull-Merge-Push trên branch '{branch}'...", "#9C27B0")
        self.run_git_task(self.git_manager.pull_merge_push, token, msg, branch)

    def do_rollback(self):
        # Verify thư mục trước khi thao tác
        ok, err_msg = self._verify_project_dir()
        if not ok:
            QMessageBox.warning(self, "Lỗi", err_msg)
            return
        
        self.save_settings()
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Thiếu Token", "Bạn cần nhập Github Personal Access Token để thực hiện thao tác nguy hiểm này!")
            return
        
        reply = QMessageBox.question(
            self, "Xác nhận Rollback", 
            "CẢNH BÁO: Thao tác này sẽ XÓA commit cuối cùng trên GitHub.\n"
            "Dữ liệu code tại commit đó sẽ mất vĩnh viễn.\n\n"
            "Bạn có chắc chắn muốn tiếp tục không?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No: return

        branch = self.branch_input.text().strip() or "main"
        self.log(f"⏳ Đang Rollback commit trên branch '{branch}'...", "#da3633")
        self.run_git_task(self.git_manager.rollback_last_push, token, branch)

    def do_switch_branch(self):
        branch = self.branch_input.text().strip()
        if not branch:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên branch!")
            return
        
        ok, msg = self.git_manager.switch_branch(branch)
        if ok:
            self.log(f"🌿 {msg}", "#2196F3")
            QMessageBox.information(self, "Branch", msg)
        else:
            self.log(f"❌ {msg}", "#d32f2f")
            QMessageBox.critical(self, "Lỗi", msg)

    def do_delete_branch(self):
        branch = self.branch_input.text().strip()
        if not branch:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tên branch cần xóa!")
            return
            
        if branch in ["main", "master"]:
            QMessageBox.critical(self, "Lỗi", "Không được phép xóa nhánh chính (main/master)!")
            return
            
        token = self.token_input.text().strip()
        if not token:
            QMessageBox.warning(self, "Thiếu Token", "Bạn cần nhập Token để xóa branch trên GitHub!")
            return

        reply = QMessageBox.critical(
            self, "Xác nhận xóa nhánh", 
            f"CẢNH BÁO: Bạn có chắc chắn muốn XÓA VĨNH VIỄN nhánh '{branch}' trên GitHub không?\n\n"
            "Hành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.No: return
        
        self.log(f"⏳ Đang xóa branch '{branch}' trên GitHub...", "#da3633")
        self.run_git_task(self.git_manager.delete_remote_branch, token, branch)