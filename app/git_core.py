# app/git_core.py
import os
import git
from git import Repo, GitCommandError
class GitManager:
    # Danh sách các pattern cần loại bỏ khỏi Git tracking
    IGNORED_PATTERNS = [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        "*.pyd",
        ".venv",
        "venv",
        "env",
        ".env",
        "build",
        "dist",
        "*.spec",
    ]
    
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.repo = None
    
    def _remove_ignored_from_tracking(self):
        """Xóa các file/thư mục trong .gitignore ra khỏi Git tracking.
        Điều này đảm bảo các file đã ignore sẽ không bị push lên remote,
        kể cả khi chúng đã được commit trước khi thêm .gitignore.
        """
        if not self.repo:
            return
        try:
            for pattern in self.IGNORED_PATTERNS:
                try:
                    # Sử dụng git rm --cached để bỏ tracking (giữ file trên disk)
                    self.repo.git.rm("-r", "--cached", "--ignore-unmatch", pattern)
                except Exception:
                    pass  # Bỏ qua nếu pattern không tồn tại
        except Exception:
            pass  # Bỏ qua lỗi để không làm gián đoạn quy trình chính
    def init_or_load_repo(self):
        try:
            if os.path.exists(os.path.join(self.project_dir, ".git")):
                self.repo = Repo(self.project_dir)
                return True, "Repository loaded."
            else:
                self.repo = Repo.init(self.project_dir)
                with self.repo.config_writer() as git_config:
                    if not git_config.has_option('user', 'email'):
                        git_config.set_value('user', 'email', 'user@codepatcher.local')
                        git_config.set_value('user', 'name', 'CodePatcher User')
                return True, "New repository initialized."
        except Exception as e:
            return False, str(e)
    def set_remote(self, remote_url):
        if not self.repo: return False, "Repository not initialized."
        try:
            if 'origin' in self.repo.remotes:
                self.repo.delete_remote('origin')
            self.repo.create_remote('origin', remote_url)
            return True, f"Remote set: {remote_url}"
        except Exception as e:
            return False, str(e)
    def _sanitize_error(self, error_msg, token):
        """Loại bỏ token khỏi error message để tránh leak credentials."""
        if token and token in str(error_msg):
            return str(error_msg).replace(token, "***TOKEN***")
        return str(error_msg)

    def _ensure_gitignore(self):
        """Đảm bảo file .gitignore tồn tại và chứa các pattern cần thiết."""
        gitignore_path = os.path.join(self.project_dir, ".gitignore")
        existing_patterns = set()
        
        if os.path.exists(gitignore_path):
            try:
                with open(gitignore_path, "r", encoding="utf-8") as f:
                    existing_patterns = set(line.strip() for line in f if line.strip())
            except Exception:
                pass
        
        new_patterns = []
        for pattern in self.IGNORED_PATTERNS:
            if pattern not in existing_patterns:
                new_patterns.append(pattern)
        
        if new_patterns:
            try:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    if existing_patterns and not os.path.getsize(gitignore_path) == 0:
                         # Nếu file không rỗng và không kết thúc bằng newline, thêm newline trước
                        with open(gitignore_path, "rb") as rb:
                            rb.seek(-1, 2)
                            if rb.read(1) != b'\n':
                                f.write("\n")
                    
                    for pattern in new_patterns:
                        f.write(f"{pattern}\n")
            except Exception:
                pass

    def pull_code(self, token, branch="main"):
        if not self.repo: return False, "Repository not loaded."
        try:
            # Check if origin remote exists
            if 'origin' not in self.repo.remotes:
                return False, "Remote 'origin' chưa được cấu hình. Vui lòng kết nối Git trước."
            
            git_dir = os.path.join(self.project_dir, ".git")
            if os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
                try: self.repo.git.merge("--abort")
                except: pass
            remote_url = self.repo.remotes.origin.url
            if "https://" in remote_url and "@" not in remote_url and token:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
            else:
                auth_url = remote_url
            self.repo.git.pull(auth_url, branch, "--allow-unrelated-histories", "-X", "theirs")
            self.repo.git.reset("--hard", "HEAD")
            return True, "Pull & Reset successful."
        except GitCommandError as e:
            try: self.repo.git.merge("--abort")
            except: pass
            return False, f"Pull Error: {self._sanitize_error(e, token)}"
        except Exception as e:
            return False, f"Unknown Error: {self._sanitize_error(e, token)}"
    def push_code(self, token, commit_msg="Auto update from CodePatcher", branch="main"):
        if not self.repo: return False, "Repository not loaded."
        try:
            # Check if origin remote exists
            if 'origin' not in self.repo.remotes:
                return False, "Remote 'origin' chưa được cấu hình. Vui lòng kết nối Git trước."
            
            try:
                git_dir = os.path.join(self.project_dir, ".git")
                if os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
                    self.repo.git.merge("--abort") 
            except:
                pass
            
            # Đảm bảo .gitignore tồn tại và chứa các pattern cần thiết
            self._ensure_gitignore()
            
            # Xóa các file/thư mục ignored ra khỏi tracking trước khi add
            self._remove_ignored_from_tracking()
            self.repo.git.add(A=True)
            if self.repo.is_dirty(untracked_files=True) or len(self.repo.heads) == 0:
                self.repo.index.commit(commit_msg)
            if branch not in self.repo.heads:
                self.repo.git.checkout("-b", branch)
            remote_url = self.repo.remotes.origin.url
            if "https://" in remote_url and "@" not in remote_url:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
            else:
                auth_url = remote_url
            self.repo.git.push("-f", "-u", auth_url, branch)
            return True, "Force Push successful."
        except GitCommandError as e:
            return False, f"Push Error: {self._sanitize_error(e, token)}"
        except Exception as e:
            return False, f"Error: {self._sanitize_error(e, token)}"

    def pull_merge_push(self, token, commit_msg="Auto update from CodePatcher", branch="main"):
        """Pull code từ remote, merge với local changes, rồi push (không force)."""
        if not self.repo: return False, "Repository not loaded."
        try:
            # Check if origin remote exists
            if 'origin' not in self.repo.remotes:
                return False, "Remote 'origin' chưa được cấu hình. Vui lòng kết nối Git trước."
            
            # Abort any pending merge
            try:
                git_dir = os.path.join(self.project_dir, ".git")
                if os.path.exists(os.path.join(git_dir, "MERGE_HEAD")):
                    self.repo.git.merge("--abort") 
            except:
                pass
            
            # Đảm bảo .gitignore tồn tại và chứa các pattern cần thiết
            self._ensure_gitignore()

            # Xóa các file/thư mục ignored ra khỏi tracking trước khi add
            self._remove_ignored_from_tracking()
            
            # Stage and commit local changes first
            self.repo.git.add(A=True)
            if self.repo.is_dirty(untracked_files=True) or len(self.repo.heads) == 0:
                self.repo.index.commit(commit_msg)
            
            # Ensure we're on the correct branch
            if branch not in self.repo.heads:
                self.repo.git.checkout("-b", branch)
            else:
                self.repo.git.checkout(branch)
            
            # Build authenticated URL
            remote_url = self.repo.remotes.origin.url
            if "https://" in remote_url and "@" not in remote_url and token:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
            else:
                auth_url = remote_url
            
            # Fetch from remote
            self.repo.git.fetch(auth_url, branch)
            
            # Try to merge remote changes
            try:
                self.repo.git.merge(f"FETCH_HEAD", "--no-edit", "--allow-unrelated-histories")
            except GitCommandError as merge_error:
                # If merge conflict, abort and notify user
                try:
                    self.repo.git.merge("--abort")
                except:
                    pass
                return False, f"Merge conflict! Vui lòng giải quyết conflict thủ công hoặc dùng Force Push.\nChi tiết: {self._sanitize_error(merge_error, token)}"
            
            # Push to remote (no force)
            self.repo.git.push("-u", auth_url, branch)
            return True, "Pull-Merge-Push successful! Code đã được đồng bộ an toàn."
        except GitCommandError as e:
            try:
                self.repo.git.merge("--abort")
            except:
                pass
            return False, f"Pull-Merge-Push Error: {self._sanitize_error(e, token)}"
        except Exception as e:
            return False, f"Error: {self._sanitize_error(e, token)}"

    def rollback_last_push(self, token, branch="main"):
        if not self.repo: return False, "Repository not loaded."
        try:
            # Check if origin remote exists
            if 'origin' not in self.repo.remotes:
                return False, "Remote 'origin' chưa được cấu hình. Vui lòng kết nối Git trước."
            
            # Check if there are enough commits to rollback
            try:
                commit_count = len(list(self.repo.iter_commits(branch, max_count=2)))
                if commit_count < 2:
                    return False, f"Không thể rollback: Branch '{branch}' chỉ có {commit_count} commit."
            except Exception:
                return False, f"Không thể đọc lịch sử commits của branch '{branch}'."
            
            remote_url = self.repo.remotes.origin.url
            if "https://" in remote_url and "@" not in remote_url and token:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
            else:
                auth_url = remote_url
            self.repo.git.reset("--hard", "HEAD~1")
            self.repo.git.push("-f", auth_url, branch)
            return True, "Rollback successful (Last commit deleted from Remote)."
        except Exception as e:
            return False, f"Rollback Error: {self._sanitize_error(e, token)}"

    def switch_branch(self, branch):
        """Chuyển sang branch khác hoặc tạo mới nếu chưa có."""
        if not self.repo: return False, "Repository not loaded."
        try:
            # Refresh lại danh sách branch từ remote
            try: self.repo.git.fetch()
            except: pass
            
            if branch in self.repo.heads:
                self.repo.git.checkout(branch)
                return True, f"Đã chuyển sang branch: {branch}"
            else:
                self.repo.git.checkout("-b", branch)
                return True, f"Đã tạo và chuyển sang branch mới: {branch}"
        except Exception as e:
            return False, f"Lỗi chuyển branch: {str(e)}"

    def delete_remote_branch(self, token, branch):
        """Xóa một branch trên remote (GitHub)."""
        if not self.repo: return False, "Repository not loaded."
        if branch in ["main", "master"]:
            return False, f"Không được phép xóa nhánh bảo vệ: {branch}"
            
        try:
            remote_url = self.repo.remotes.origin.url
            if "https://" in remote_url and "@" not in remote_url:
                auth_url = remote_url.replace("https://", f"https://oauth2:{token}@")
            else:
                auth_url = remote_url
                
            # Lệnh xóa branch trên remote: git push origin --delete <branch>
            self.repo.git.push(auth_url, "--delete", branch)
            return True, f"Đã xóa branch '{branch}' trên GitHub thành công."
        except Exception as e:
            return False, f"Lỗi khi xóa branch: {self._sanitize_error(e, token)}"