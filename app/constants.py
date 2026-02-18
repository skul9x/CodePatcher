# app/constants.py
import re

APP_TITLE = "CodePatcher v3.2 - CyberNord Edition"
WINDOW_ICON_NAME = "SP_ComputerIcon"
BACKUP_DIR_NAME = ".patch_backups"

APP_FONT_FAMILY = "Inter, Roboto, Ubuntu, Segoe UI, sans-serif"
APP_FONT_SIZE = 10

STATUS_FOUND = "Đã tìm thấy"
STATUS_NEW = "Tạo file mới"
STATUS_NOT_FOUND = "Không tìm thấy"
STATUS_UNSAFE = "Đường dẫn không an toàn"

PATCH_REGEX = re.compile(r"```[^\n]*\n(.*?)\n```", re.DOTALL)